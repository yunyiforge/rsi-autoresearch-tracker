"""RSS 2.0 / RSS 1.0 (RDF) / Atom collector for blogs and newsletters."""
from __future__ import annotations

import re
import time
import xml.etree.ElementTree as ET
from urllib.parse import urljoin

from ..models import make_item
from ..textutil import canonical_url, short_hash, strip_html, to_iso

_BAD_ENTITY = re.compile(rb"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)")


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def _child(el, name: str):
    for c in el:
        if _local(c.tag) == name:
            return c
    return None


def _text(el, *names: str) -> str:
    for name in names:
        c = _child(el, name)
        if c is not None and (c.text or "").strip():
            return c.text.strip()
    return ""


def _parse_xml(data: bytes):
    try:
        return ET.fromstring(data)
    except ET.ParseError:
        # Many feeds embed HTML entities such as &nbsp; that XML does not define.
        return ET.fromstring(_BAD_ENTITY.sub(b"&amp;", data))


def parse_feed(data: bytes, base_url: str = "") -> list[dict]:
    root = _parse_xml(data)
    entries = []
    if _local(root.tag) == "feed":  # Atom
        for e in root:
            if _local(e.tag) != "entry":
                continue
            link = ""
            for c in e:
                if _local(c.tag) == "link" and c.get("rel") in (None, "alternate") and c.get("href"):
                    link = c.get("href")
                    break
            author = _child(e, "author")
            entries.append({
                "title": strip_html(_text(e, "title")),
                "link": link,
                "summary": strip_html(_text(e, "summary", "content")),
                "published": to_iso(_text(e, "published", "updated")),
                "author": _text(author, "name") if author is not None else "",
            })
    else:  # RSS 2.0 / RDF
        for e in root.iter():
            if _local(e.tag) != "item":
                continue
            entries.append({
                "title": strip_html(_text(e, "title")),
                "link": _text(e, "link", "guid"),
                "summary": strip_html(_text(e, "description", "encoded", "summary")),
                "published": to_iso(_text(e, "pubDate", "date", "published", "updated")),
                "author": _text(e, "creator", "author"),
            })
    for x in entries:
        if x["link"] and base_url:
            x["link"] = urljoin(base_url, x["link"])
    return [x for x in entries if x["title"] and x["link"].startswith("http")]


def entry_to_item(entry: dict, feed_name: str) -> dict:
    return make_item(
        id=f"url:{short_hash(canonical_url(entry['link']))}",
        source="rss",
        type="article",
        title=entry["title"],
        url=entry["link"],
        summary=entry["summary"],
        authors=[entry["author"]] if entry["author"] else [],
        published=entry["published"],
        extra={"feed": feed_name},
    )


def collect(cfg: dict, client, log) -> dict:
    items, errors = [], []
    cutoff = time.strftime("%Y-%m-%dT%H:%M:%SZ",
                           time.gmtime(time.time() - 86400 * int(cfg.get("lookback_days", 60))))
    limit = int(cfg.get("max_items_per_feed", 50))
    for feed in cfg.get("feeds") or []:
        name, url = feed.get("name") or feed.get("url"), feed.get("url")
        try:
            entries = parse_feed(client.get(url, headers={
                "Accept": "application/rss+xml, application/atom+xml, application/xml;q=0.9, */*;q=0.8"}), base_url=url)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{name}: {e}")
            log(f"  [rss] feed failed: {name}: {e}")
            continue
        fresh = [e for e in entries if not e["published"] or e["published"] >= cutoff][:limit]
        log(f"  [rss] {name}: {len(entries)} entries, {len(fresh)} within lookback")
        items.extend(entry_to_item(e, name) for e in fresh)
    return {"items": items, "errors": errors}

"""arXiv Atom API collector (https://info.arxiv.org/help/api/)."""
from __future__ import annotations

import time
import xml.etree.ElementTree as ET

from ..models import make_item, query_spec
from ..textutil import arxiv_id_from_url, clean_ws, find_github_repos, to_iso

API = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"


def build_search_query(q: str, categories: list[str] | None) -> str:
    query = q if ":" in q else f'all:"{q}"'
    if categories:
        cats = " OR ".join(f"cat:{c}" for c in categories)
        query = f"({query}) AND ({cats})"
    return query


def parse_feed(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    entries = []
    for entry in root.findall(f"{ATOM}entry"):
        aid = arxiv_id_from_url(entry.findtext(f"{ATOM}id") or "")
        if not aid:
            continue
        summary = clean_ws(entry.findtext(f"{ATOM}summary"))
        comment = clean_ws(entry.findtext(f"{ARXIV}comment"))
        primary = entry.find(f"{ARXIV}primary_category")
        pdf = None
        for link in entry.findall(f"{ATOM}link"):
            if link.get("title") == "pdf":
                pdf = link.get("href")
        entries.append({
            "arxiv_id": aid,
            "title": clean_ws(entry.findtext(f"{ATOM}title")),
            "summary": summary,
            "comment": comment,
            "authors": [clean_ws(a.findtext(f"{ATOM}name")) for a in entry.findall(f"{ATOM}author")],
            "published": to_iso(entry.findtext(f"{ATOM}published")),
            "updated": to_iso(entry.findtext(f"{ATOM}updated")),
            "primary_category": primary.get("term") if primary is not None else None,
            "categories": [c.get("term") for c in entry.findall(f"{ATOM}category") if c.get("term")],
            "pdf": pdf,
            "code_repos": find_github_repos(f"{summary} {comment}"),
        })
    return entries


def entry_to_item(e: dict, topic: str | None = None) -> dict:
    aid = e["arxiv_id"]
    return make_item(
        id=f"arxiv:{aid}",
        source="arxiv",
        type="paper",
        title=e["title"],
        url=f"https://arxiv.org/abs/{aid}",
        summary=e["summary"],
        authors=e["authors"],
        published=e["published"],
        updated=e["updated"],
        links={
            "pdf": e["pdf"] or f"https://arxiv.org/pdf/{aid}",
            "code": [f"https://github.com/{r}" for r in e["code_repos"]],
        },
        extra={
            "primary_category": e["primary_category"],
            "categories": e["categories"],
            "comment": e["comment"],
            "code_repos": e["code_repos"],
        },
        query_topics=[topic] if topic else [],
    )


def collect(cfg: dict, client, log) -> dict:
    items, errors = [], []
    categories = cfg.get("categories") or []
    max_results = int(cfg.get("max_results", 50))
    delay = float(cfg.get("delay_seconds", 3.5))
    for i, raw in enumerate(cfg.get("queries") or []):
        spec = query_spec(raw)
        if i:
            time.sleep(delay)
        params = {
            "search_query": build_search_query(spec["q"], categories),
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        try:
            entries = parse_feed(client.get(API, params=params))
        except Exception as e:  # noqa: BLE001 - one bad query must not kill the run
            errors.append(f"{spec['q']}: {e}")
            log(f"  [arxiv] query failed: {spec['q']}: {e}")
            continue
        log(f"  [arxiv] {spec['q']!r}: {len(entries)} entries")
        items.extend(entry_to_item(e, spec.get("topic")) for e in entries)
    return {"items": items, "errors": errors}

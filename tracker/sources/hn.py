"""Hacker News collector via the Algolia search API (https://hn.algolia.com/api)."""
from __future__ import annotations

import time

from ..models import make_item, query_spec
from ..textutil import strip_html, to_iso

API = "https://hn.algolia.com/api/v1/search_by_date"


def hit_to_item(hit: dict, topic: str | None = None) -> dict | None:
    oid = str(hit.get("objectID") or "")
    title = hit.get("title") or hit.get("story_title")
    if not oid or not title:
        return None
    discussion = f"https://news.ycombinator.com/item?id={oid}"
    return make_item(
        id=f"hn:{oid}",
        source="hn",
        type="discussion",
        title=title,
        url=hit.get("url") or discussion,
        summary=strip_html(hit.get("story_text") or ""),
        authors=[hit.get("author")],
        published=to_iso(hit.get("created_at_i") or hit.get("created_at")),
        metrics={"points": hit.get("points") or 0, "comments": hit.get("num_comments") or 0},
        links={"discussion": discussion},
        query_topics=[topic] if topic else [],
    )


def collect(cfg: dict, client, log) -> dict:
    items, errors = [], []
    since = int(time.time() - 86400 * int(cfg.get("lookback_days", 30)))
    min_points = int(cfg.get("min_points", 5))
    for raw in cfg.get("queries") or []:
        spec = query_spec(raw)
        params = {
            "query": spec["q"],
            "tags": "story",
            "hitsPerPage": int(cfg.get("hits_per_page", 50)),
            "numericFilters": f"created_at_i>{since},points>={min_points}",
        }
        try:
            data = client.get_json(API, params=params)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{spec['q']}: {e}")
            log(f"  [hn] query failed: {spec['q']}: {e}")
            continue
        hits = data.get("hits") or []
        log(f"  [hn] {spec['q']!r}: {len(hits)} stories")
        for hit in hits:
            item = hit_to_item(hit, spec.get("topic"))
            if item:
                items.append(item)
        time.sleep(0.3)
    return {"items": items, "errors": errors}

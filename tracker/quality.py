"""Schema / consistency checks run before anything is written."""
from __future__ import annotations

import re

from .models import ID_PREFIX, SOURCES, TYPES

ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SOURCE_TYPE = {"arxiv": "paper", "github": "repo", "hn": "discussion", "rss": "article"}


def item_problems(item: dict) -> list[str]:
    p = []
    for key in ("id", "source", "type", "title", "url", "first_seen", "last_seen"):
        if not isinstance(item.get(key), str) or not item.get(key):
            p.append(f"missing/empty {key}")
    for key in ("topics", "tags", "authors", "related_ids", "query_topics"):
        if not isinstance(item.get(key), list):
            p.append(f"{key} must be a list")
    for key in ("metrics", "links", "extra"):
        if not isinstance(item.get(key), dict):
            p.append(f"{key} must be an object")
    src = item.get("source")
    if src not in SOURCES:
        p.append(f"unknown source {src!r}")
    else:
        if not str(item.get("id", "")).startswith(ID_PREFIX[src]):
            p.append(f"id must start with {ID_PREFIX[src]!r}")
        if item.get("type") != SOURCE_TYPE[src]:
            p.append(f"type {item.get('type')!r} inconsistent with source {src}")
    if item.get("type") not in TYPES:
        p.append(f"unknown type {item.get('type')!r}")
    if not str(item.get("url", "")).startswith(("http://", "https://")):
        p.append("url must be http(s)")
    for key in ("published", "updated", "first_seen", "last_seen"):
        v = item.get(key)
        if v is not None and not ISO_RE.match(str(v)):
            p.append(f"{key} not ISO-8601 UTC: {v!r}")
    if not item.get("topics"):
        p.append("no topics")
    return p


def check_items(store: dict[str, dict]) -> tuple[list[str], dict]:
    """Drop invalid items in place; return (dropped-item messages, summary)."""
    dropped = []
    for item_id in list(store):
        problems = item_problems(store[item_id])
        if problems:
            dropped.append(f"{item_id}: {'; '.join(problems)}")
            del store[item_id]
    urls: dict[tuple, str] = {}
    dup_urls = 0
    for it in store.values():
        key = (it["source"], it["url"])
        if key in urls:
            dup_urls += 1
        urls[key] = it["id"]
    return dropped, {"invalid_dropped": len(dropped), "duplicate_urls_within_source": dup_urls}


def check_records(records: list[dict], kind: str, id_key: str = "id") -> list[str]:
    errors, seen = [], set()
    for r in records:
        rid = r.get(id_key)
        if not rid:
            errors.append(f"{kind}: record without {id_key}: {r}")
            continue
        if rid in seen:
            errors.append(f"{kind}: duplicate {id_key} {rid}")
        seen.add(rid)
        if kind != "benchmark_tasks":
            if not r.get("name"):
                errors.append(f"{kind}: {rid} has no name")
            if r.get("status") not in ("curated", "candidate"):
                errors.append(f"{kind}: {rid} bad status {r.get('status')!r}")
            if r.get("status") == "curated" and not (r.get("url") or r.get("repo") or r.get("arxiv_id") or r.get("homepage")):
                errors.append(f"{kind}: {rid} has no url/repo/arxiv_id")
    return errors

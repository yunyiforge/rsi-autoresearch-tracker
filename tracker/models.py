"""Unified item schema shared by all sources."""
from __future__ import annotations

from .textutil import clean_ws, truncate

SOURCES = ("arxiv", "github", "hn", "rss")
TYPES = ("paper", "repo", "discussion", "article")
ID_PREFIX = {"arxiv": "arxiv:", "github": "github:", "hn": "hn:", "rss": "url:"}

SUMMARY_LIMIT = 2000


def make_item(*, id: str, source: str, type: str, title: str, url: str, summary: str = "",
              authors: list[str] | None = None, published: str | None = None,
              updated: str | None = None, metrics: dict | None = None,
              links: dict | None = None, extra: dict | None = None,
              query_topics: list[str] | None = None) -> dict:
    return {
        "id": id,
        "source": source,
        "type": type,
        "title": clean_ws(title),
        "url": url,
        "summary": truncate(clean_ws(summary), SUMMARY_LIMIT),
        "authors": [a for a in (authors or []) if a],
        "published": published,
        "updated": updated,
        "first_seen": None,
        "last_seen": None,
        "topics": [],
        "tags": [],
        "relevance": 0,
        "metrics": metrics or {},
        "links": {k: v for k, v in (links or {}).items() if v},
        "related_ids": [],
        "query_topics": sorted(set(t for t in (query_topics or []) if t)),
        "extra": extra or {},
    }


def query_spec(q) -> dict:
    """Queries in config may be a plain string or a dict {q, topic, ...}."""
    if isinstance(q, dict):
        spec = dict(q)
        spec["q"] = str(spec.get("q", ""))
        return spec
    return {"q": str(q)}

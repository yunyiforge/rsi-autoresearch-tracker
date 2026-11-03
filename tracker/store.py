"""JSONL/JSON/CSV persistence plus incremental merge, de-duplication and cross-linking."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from .textutil import arxiv_id_from_url, canonical_url, github_repo_from_url, normalize_text


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: ("; ".join(map(str, v)) if isinstance(v, list) else v) for k, v in row.items()})


def merge_items(store: dict[str, dict], collected: list[dict], now: str) -> list[str]:
    """Merge newly collected items into the store in place. Returns ids first seen in this run."""
    new_ids = []
    for item in collected:
        old = store.get(item["id"])
        if old is None:
            item["first_seen"] = now
            item["last_seen"] = now
            store[item["id"]] = item
            new_ids.append(item["id"])
            continue
        old["last_seen"] = now
        for key in ("title", "url", "summary", "published", "updated"):
            if item.get(key):
                old[key] = item[key]
        if item.get("authors"):
            old["authors"] = item["authors"]
        old.setdefault("metrics", {}).update(item.get("metrics") or {})
        old["links"] = {**(old.get("links") or {}), **(item.get("links") or {})}
        old["extra"] = {**(old.get("extra") or {}), **(item.get("extra") or {})}
        old["query_topics"] = sorted(set(old.get("query_topics") or []) | set(item.get("query_topics") or []))
    return new_ids


def _engagement(item: dict) -> int:
    m = item.get("metrics") or {}
    return int(m.get("points") or 0) + int(m.get("stars") or 0)


def dedupe(store: dict[str, dict]) -> int:
    """Remove near-duplicate discussions/articles (same canonical URL or same title). Returns count removed."""
    removed = 0
    for key_fn in (lambda it: canonical_url(it.get("url")), lambda it: normalize_text(it.get("title"))):
        groups: dict[tuple, list[dict]] = {}
        for item in store.values():
            if item["source"] not in ("hn", "rss"):
                continue
            key = key_fn(item)
            if key:
                groups.setdefault((item["source"], key), []).append(item)
        for dupes in groups.values():
            if len(dupes) < 2:
                continue
            dupes.sort(key=lambda it: (-_engagement(it), it.get("first_seen") or "", it["id"]))
            keep = dupes[0]
            for d in dupes[1:]:
                keep["first_seen"] = min(keep.get("first_seen") or d["first_seen"], d.get("first_seen") or keep["first_seen"])
                aliases = set(keep.get("extra", {}).get("duplicate_ids") or []) | {d["id"]}
                keep.setdefault("extra", {})["duplicate_ids"] = sorted(aliases)
                store.pop(d["id"], None)
                removed += 1
    return removed


def link_related(store: dict[str, dict]) -> int:
    """Cross-link items across sources (HN/blog -> paper/repo, paper -> code repo). Returns link count."""
    url_index = {canonical_url(it["url"]): it["id"] for it in store.values() if it["source"] in ("arxiv", "github", "rss")}
    for it in store.values():
        it["related_ids"] = []
        (it.get("links") or {}).pop("discussions", None)
    links = 0
    for it in store.values():
        targets = set()
        if it["source"] in ("hn", "rss"):
            aid = arxiv_id_from_url(it["url"])
            if aid and f"arxiv:{aid}" in store:
                targets.add(f"arxiv:{aid}")
            repo = github_repo_from_url(it["url"])
            if repo and f"github:{repo.lower()}" in store:
                targets.add(f"github:{repo.lower()}")
            other = url_index.get(canonical_url(it["url"]))
            if other and other != it["id"]:
                targets.add(other)
        if it["source"] == "arxiv":
            for repo in (it.get("extra") or {}).get("code_repos") or []:
                if f"github:{repo.lower()}" in store:
                    targets.add(f"github:{repo.lower()}")
        for t in sorted(targets):
            it["related_ids"].append(t)
            target = store[t]
            if it["id"] not in target["related_ids"]:
                target["related_ids"].append(it["id"])
            if it["source"] in ("hn", "rss"):
                ref = (it.get("links") or {}).get("discussion") or it["url"]
                target.setdefault("links", {}).setdefault("discussions", [])
                if ref not in target["links"]["discussions"]:
                    target["links"]["discussions"].append(ref)
            links += 1
    for it in store.values():
        it["related_ids"] = sorted(set(it["related_ids"]))
    return links


def sort_items(items) -> list[dict]:
    return sorted(items, key=lambda it: (it.get("published") or it.get("first_seen") or "", it["id"]), reverse=True)

"""GitHub Search / Repos API collector. Uses GITHUB_TOKEN (or GH_TOKEN) if present."""
from __future__ import annotations

import os
import time

from ..http import HttpError
from ..models import make_item, query_spec
from ..textutil import to_iso

API = "https://api.github.com"


def api_headers() -> dict:
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def repo_to_item(r: dict, topic: str | None = None) -> dict:
    full = r["full_name"]
    return make_item(
        id=f"github:{full.lower()}",
        source="github",
        type="repo",
        title=full,
        url=r.get("html_url") or f"https://github.com/{full}",
        summary=r.get("description") or "",
        authors=[(r.get("owner") or {}).get("login")],
        published=to_iso(r.get("created_at")),
        updated=to_iso(r.get("pushed_at")),
        metrics={
            "stars": r.get("stargazers_count", 0),
            "forks": r.get("forks_count", 0),
            "open_issues": r.get("open_issues_count", 0),
        },
        links={"homepage": r.get("homepage") or None},
        extra={
            "language": r.get("language"),
            "topics": r.get("topics") or [],
            "license": (r.get("license") or {}).get("spdx_id"),
            "archived": bool(r.get("archived")),
        },
        query_topics=[topic] if topic else [],
    )


def fetch_repo(client, full_name: str) -> dict | None:
    """Return repo JSON, or None if the repo does not exist (404)."""
    try:
        return client.get_json(f"{API}/repos/{full_name}", headers=api_headers())
    except HttpError as e:
        if e.code == 404:
            return None
        raise


def collect(cfg: dict, client, log) -> dict:
    items, errors = [], []
    per_page = int(cfg.get("per_page", 50))
    default_min_stars = int(cfg.get("min_stars", 10))
    delay = float(cfg.get("delay_seconds", 2.5))
    if not (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")):
        log("  [github] no GITHUB_TOKEN: unauthenticated search is limited to 10 req/min")
        delay = max(delay, 7.0)
    for i, raw in enumerate(cfg.get("queries") or []):
        spec = query_spec(raw)
        q = spec["q"]
        if "stars:" not in q:
            q = f"{q} stars:>={int(spec.get('min_stars', default_min_stars))}"
        if i:
            time.sleep(delay)
        params = {"q": q, "sort": spec.get("sort", "stars"), "order": "desc", "per_page": per_page}
        try:
            data = client.get_json(f"{API}/search/repositories", params=params, headers=api_headers())
        except Exception as e:  # noqa: BLE001
            errors.append(f"{q}: {e}")
            log(f"  [github] query failed: {q}: {e}")
            continue
        repos = data.get("items") or []
        log(f"  [github] {q!r}: {len(repos)} repos")
        items.extend(repo_to_item(r, spec.get("topic")) for r in repos)
    return {"items": items, "errors": errors}

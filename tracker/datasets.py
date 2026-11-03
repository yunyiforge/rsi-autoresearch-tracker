"""Build curated + auto-discovered datasets: frameworks, benchmarks, benchmark task candidates."""
from __future__ import annotations

import re

from .classify import Classifier
from .textutil import KeywordMatcher, normalize_text, slugify, truncate

BENCH_TITLE_RE = re.compile(r"bench|leaderboard|\barena\b|evaluation suite|\bgym\b", re.I)
BENCH_DESC_RE = re.compile(r"^\W*(?:[\w-]+\s*(?:is|:|-)\s*)?(?:a|an|the)\s+(?:[\w-]+\s+){0,3}(?:benchmark|evaluation suite|leaderboard)\b", re.I)
BENCH_NAME_RE = re.compile(r"\b([A-Za-z0-9][\w.+-]*(?:[Bb]ench|BENCH|Gym|Arena)[\w.+-]*)")

FRAMEWORK_FIELDS = ["id", "name", "category", "topics", "status", "source", "org", "repo", "url",
                    "arxiv_id", "year", "stars", "forks", "language", "license", "last_push",
                    "repo_status", "description", "first_seen", "last_seen", "evidence"]
BENCHMARK_FIELDS = ["id", "name", "focus", "topics", "status", "source", "org", "arxiv_id", "paper_url",
                    "repo", "homepage", "year", "tasks", "metric", "stars", "repo_status",
                    "description", "first_seen", "last_seen", "evidence"]
TASK_FIELDS = ["task_id", "task_type", "status", "difficulty_hint", "topics", "tags", "paper",
               "code_repos", "instructions", "grading", "source_item", "first_seen"]


def _year(iso: str | None):
    return int(iso[:4]) if iso and iso[:4].isdigit() else None


def _apply_repo_meta(rec: dict, meta: dict | None, prev: dict | None) -> None:
    """meta: GitHub repo JSON, {} = repo confirmed missing, None = not fetched (fall back to prev)."""
    if meta:
        rec.update({
            "stars": meta.get("stargazers_count"),
            "forks": meta.get("forks_count"),
            "language": meta.get("language"),
            "license": (meta.get("license") or {}).get("spdx_id"),
            "last_push": meta.get("pushed_at"),
            "repo_status": "archived" if meta.get("archived") else "ok",
        })
        if meta.get("full_name") and meta["full_name"].lower() != (rec.get("repo") or "").lower():
            rec["repo_moved_to"] = meta["full_name"]
    elif meta == {}:
        rec["repo_status"] = "not_found"
    elif prev:
        for k in ("stars", "forks", "language", "license", "last_push", "repo_status", "repo_moved_to"):
            if prev.get(k) is not None:
                rec[k] = prev[k]


def _item_repo_meta(item: dict | None) -> dict | None:
    """Turn a collected GitHub item into the subset of repo JSON used by _apply_repo_meta."""
    if not item:
        return None
    m, e = item.get("metrics") or {}, item.get("extra") or {}
    return {"stargazers_count": m.get("stars"), "forks_count": m.get("forks"),
            "language": e.get("language"), "license": {"spdx_id": e.get("license")},
            "pushed_at": item.get("updated"), "archived": e.get("archived"), "full_name": item.get("title")}


def _seen(rec: dict, prev: dict | None, now: str) -> None:
    rec["first_seen"] = (prev or {}).get("first_seen") or now
    rec["last_seen"] = now


def _repo_key(repo: str | None) -> str:
    return f"github:{repo.lower()}" if repo else ""


def build_frameworks(cfg: dict, store: dict, repo_meta: dict, prev: list[dict], now: str,
                     classifier: Classifier) -> list[dict]:
    prev_by_id = {r["id"]: r for r in prev}
    dcfg = (cfg.get("datasets") or {}).get("frameworks") or {}
    records, curated_repos = [], set()
    for c in cfg.get("curated_frameworks") or []:
        repo = c.get("repo")
        rec = {
            "id": f"fw:{slugify(c['name'])}",
            "name": c["name"],
            "category": c.get("category", "other"),
            "topics": c.get("topics") or [],
            "status": "curated",
            "source": "curated",
            "org": c.get("org"),
            "repo": repo,
            "url": c.get("url") or (f"https://github.com/{repo}" if repo else None),
            "arxiv_id": str(c["arxiv_id"]) if c.get("arxiv_id") else None,
            "year": c.get("year"),
            "stars": None, "forks": None, "language": None, "license": None,
            "last_push": None, "repo_status": None,
            "description": c.get("description", ""),
            "evidence": [],
        }
        if repo:
            curated_repos.add(repo.lower())
            meta = repo_meta.get(repo.lower())
            if meta is None:
                meta = _item_repo_meta(store.get(_repo_key(repo)))
            _apply_repo_meta(rec, meta, prev_by_id.get(rec["id"]))
            if _repo_key(repo) in store:
                rec["evidence"].append(_repo_key(repo))
        if rec["arxiv_id"] and f"arxiv:{rec['arxiv_id']}" in store:
            rec["evidence"].append(f"arxiv:{rec['arxiv_id']}")
        _seen(rec, prev_by_id.get(rec["id"]), now)
        records.append(rec)

    curated_ids = {r["id"] for r in records}
    min_stars = int(dcfg.get("min_stars", 100))
    exclude = KeywordMatcher(dcfg.get("exclude_keywords"))
    candidates = []
    for it in store.values():
        if it["source"] != "github" or it["title"].lower() in curated_repos:
            continue
        stars = int((it.get("metrics") or {}).get("stars") or 0)
        if stars < min_stars or "benchmark" in it.get("tags", []):
            continue
        if exclude.matches(normalize_text(f"{it['title']} {it.get('summary', '')}")):
            continue
        rec = {
            "id": f"fw:{slugify(it['title'])}",
            "name": it["title"].split("/", 1)[-1],
            "category": classifier.first_match(dcfg.get("categories"), f"{it['title']} {it.get('summary', '')}"),
            "topics": it.get("topics", []),
            "status": "candidate",
            "source": "auto",
            "org": (it.get("authors") or [None])[0],
            "repo": it["title"],
            "url": it["url"],
            "arxiv_id": None,
            "year": _year(it.get("published")),
            "description": truncate(it.get("summary", ""), 300),
            "evidence": [it["id"]],
        }
        if rec["id"] in curated_ids:
            continue
        _apply_repo_meta(rec, _item_repo_meta(it), None)
        _seen(rec, prev_by_id.get(rec["id"]), now)
        candidates.append(rec)
    candidates.sort(key=lambda r: (-(r.get("stars") or 0), r["id"]))
    return records + candidates[: int(dcfg.get("max_candidates", 80))]


def extract_benchmark_name(title: str) -> str:
    head = title.split(":", 1)[0].strip()
    if ":" in title and len(head) <= 40 and len(head.split()) <= 5:
        return head
    m = BENCH_NAME_RE.search(title)
    if m:
        return m.group(1).strip(".,;")
    return truncate(title, 80)


def is_benchmark_item(item: dict) -> bool:
    if "benchmark" not in item.get("tags", []):
        return False
    if item["source"] == "arxiv":
        return bool(BENCH_TITLE_RE.search(item["title"]))
    if item["source"] == "github":
        # Repo name says bench/arena/gym, or the description introduces itself as "a ... benchmark".
        return bool(BENCH_TITLE_RE.search(item["title"]) or BENCH_DESC_RE.search(item.get("summary", "")))
    return False


def build_benchmarks(cfg: dict, store: dict, repo_meta: dict, prev: list[dict], now: str,
                     classifier: Classifier) -> list[dict]:
    prev_by_id = {r["id"]: r for r in prev}
    dcfg = (cfg.get("datasets") or {}).get("benchmarks") or {}
    records, known_arxiv, known_repos, known_names = [], set(), set(), set()
    for c in cfg.get("curated_benchmarks") or []:
        aid = str(c["arxiv_id"]) if c.get("arxiv_id") else None
        repo = c.get("repo")
        rec = {
            "id": f"bench:{slugify(c['name'])}",
            "name": c["name"],
            "focus": c.get("focus", "general-agent"),
            "topics": c.get("topics") or [],
            "status": "curated",
            "source": "curated",
            "org": c.get("org"),
            "arxiv_id": aid,
            "paper_url": f"https://arxiv.org/abs/{aid}" if aid else c.get("paper_url"),
            "repo": repo,
            "homepage": c.get("homepage"),
            "year": c.get("year"),
            "tasks": c.get("tasks"),
            "metric": c.get("metric"),
            "stars": None,
            "repo_status": None,
            "description": c.get("description", ""),
            "evidence": [],
        }
        if repo:
            known_repos.add(repo.lower())
            meta = repo_meta.get(repo.lower())
            if meta is None:
                meta = _item_repo_meta(store.get(_repo_key(repo)))
            _apply_repo_meta(rec, meta, prev_by_id.get(rec["id"]))
            for k in ("forks", "language", "license", "last_push"):
                rec.pop(k, None)
            if _repo_key(repo) in store:
                rec["evidence"].append(_repo_key(repo))
        if aid:
            known_arxiv.add(aid)
            if f"arxiv:{aid}" in store:
                rec["evidence"].append(f"arxiv:{aid}")
        known_names.add(normalize_text(c["name"]))
        _seen(rec, prev_by_id.get(rec["id"]), now)
        records.append(rec)

    curated_ids = {r["id"] for r in records}
    by_name: dict[str, dict] = {}
    for it in sorted(store.values(), key=lambda x: x["id"]):
        if not it.get("topics") or not is_benchmark_item(it):
            continue
        if it["source"] == "arxiv" and it["id"].split(":", 1)[1] in known_arxiv:
            continue
        if it["source"] == "github" and it["title"].lower() in known_repos:
            continue
        name = extract_benchmark_name(it["title"]) if it["source"] == "arxiv" else it["title"].split("/", 1)[-1]
        key = normalize_text(name)
        if key in known_names:
            continue
        rec = by_name.get(key)
        if rec is None:
            rec = {
                "id": f"bench:{slugify(name)}",
                "name": name,
                "focus": classifier.first_match(dcfg.get("focus"), f"{it['title']} {it.get('summary', '')}",
                                                default="general-agent"),
                "topics": it.get("topics", []),
                "status": "candidate",
                "source": "auto",
                "org": None, "arxiv_id": None, "paper_url": None, "repo": None, "homepage": None,
                "year": _year(it.get("published")),
                "tasks": None, "metric": None, "stars": None, "repo_status": None,
                "description": truncate(it.get("summary", ""), 300),
                "evidence": [],
            }
            if rec["id"] in curated_ids:
                continue
            by_name[key] = rec
        rec["evidence"].append(it["id"])
        rec["topics"] = sorted(set(rec["topics"]) | set(it.get("topics", [])))
        if it["source"] == "arxiv":
            aid = it["id"].split(":", 1)[1]
            rec["arxiv_id"], rec["paper_url"] = aid, it["url"]
            code = (it.get("extra") or {}).get("code_repos") or []
            if code and not rec["repo"]:
                rec["repo"] = code[0]
        else:
            rec["repo"] = it["title"]
            rec["stars"] = (it.get("metrics") or {}).get("stars")
            rec["repo_status"] = "archived" if (it.get("extra") or {}).get("archived") else "ok"
    candidates = list(by_name.values())
    for rec in candidates:
        _seen(rec, prev_by_id.get(rec["id"]), now)
    candidates.sort(key=lambda r: (r.get("first_seen") or "", r.get("year") or 0, r["id"]), reverse=True)
    return records + candidates[: int(dcfg.get("max_candidates", 150))]


_HARD = KeywordMatcher(["pretrain*", "large scale training", "reinforcement learning", "rlhf", "gpu*", "distributed"])
_EASY = KeywordMatcher(["prompting", "in context", "zero shot", "few shot", "evaluation only", "survey*"])


def difficulty_hint(item: dict) -> str:
    """Heuristic only: compute-heavy training -> hard; prompting/eval-only -> easy; else medium."""
    text = normalize_text(f"{item['title']} {item.get('summary', '')}")
    if _HARD.matches(text):
        return "hard"
    if _EASY.matches(text):
        return "easy"
    return "medium"


def build_benchmark_tasks(cfg: dict, store: dict, prev: list[dict], now: str) -> list[dict]:
    """PaperBench-style replication task candidates: relevant arXiv papers that link to official code."""
    dcfg = (cfg.get("datasets") or {}).get("benchmark_tasks") or {}
    if dcfg.get("enabled") is False:
        return []
    prev_by_id = {r["task_id"]: r for r in prev}
    tasks = []
    for it in store.values():
        repos = (it.get("extra") or {}).get("code_repos") or []
        if it["source"] != "arxiv" or not it.get("topics") or not repos or "survey" in it.get("tags", []):
            continue
        aid = it["id"].split(":", 1)[1]
        task_id = f"replicate:{aid}"
        tasks.append({
            "task_id": task_id,
            "task_type": "paper-replication",
            "status": "candidate",
            "difficulty_hint": difficulty_hint(it),
            "topics": it.get("topics", []),
            "tags": it.get("tags", []),
            "paper": {"arxiv_id": aid, "title": it["title"], "url": it["url"], "published": it.get("published")},
            "code_repos": [f"https://github.com/{r}" for r in repos],
            "instructions": (
                f"Reproduce the main empirical results of arXiv:{aid} (\"{it['title']}\") from the paper alone, "
                "without consulting the official code; the official repository is held out as the grading reference."
            ),
            "grading": {"type": "rubric", "rubric": None, "reference": "official-code", "status": "todo"},
            "source_item": it["id"],
            "first_seen": (prev_by_id.get(task_id) or {}).get("first_seen") or it.get("first_seen") or now,
        })
    tasks.sort(key=lambda t: (t["paper"].get("published") or "", t["task_id"]), reverse=True)
    return tasks[: int(dcfg.get("max_tasks", 500))]

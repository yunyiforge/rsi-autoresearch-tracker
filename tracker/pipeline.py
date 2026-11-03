"""End-to-end pipeline: collect -> merge -> classify -> validate -> dedupe -> link -> build -> report."""
from __future__ import annotations

import sys
import time
from collections import Counter
from pathlib import Path

from . import datasets, quality, reports, store as st
from .classify import Classifier
from .config import load_config
from .http import HttpClient
from .sources import COLLECTORS
from .sources.github import fetch_repo
from .textutil import utc_now_iso


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


class PipelineError(RuntimeError):
    pass


def _collect(cfg: dict, client: HttpClient, only: set[str]) -> tuple[list[dict], dict]:
    collected, health = [], {}
    for name, collect in COLLECTORS.items():
        scfg = cfg["sources"].get(name) or {}
        if only and name not in only:
            continue
        if not scfg.get("enabled", True):
            health[name] = {"status": "disabled", "fetched": 0, "errors": []}
            continue
        log(f"[collect] {name}")
        t0 = time.time()
        try:
            res = collect(scfg, client, log)
        except Exception as e:  # noqa: BLE001
            res = {"items": [], "errors": [f"{type(e).__name__}: {e}"]}
        status = "ok" if not res["errors"] else ("partial" if res["items"] else "failed")
        health[name] = {"status": status, "fetched": len(res["items"]), "errors": res["errors"][:10],
                        "seconds": round(time.time() - t0, 1)}
        collected.extend(res["items"])
    return collected, health


def _enrich_curated(cfg: dict, client: HttpClient, store: dict) -> tuple[dict, list[str]]:
    """Fetch repo metadata for curated frameworks/benchmarks not already present in the item store."""
    meta, errors = {}, []
    repos = {(c.get("repo") or "").lower(): c["repo"]
             for c in (cfg.get("curated_frameworks") or []) + (cfg.get("curated_benchmarks") or []) if c.get("repo")}
    for key, repo in sorted(repos.items()):
        if f"github:{key}" in store:
            continue
        try:
            data = fetch_repo(client, repo)
            meta[key] = data if data is not None else {}
        except Exception as e:  # noqa: BLE001
            errors.append(f"{repo}: {e}")
        time.sleep(0.2)
    log(f"[enrich] curated repos fetched: {len(meta)}, errors: {len(errors)}")
    return meta, errors


def run(config_dir="config", data_dir="data", reports_dir="reports", sources: set[str] | None = None,
        offline: bool = False, client: HttpClient | None = None) -> dict:
    cfg = load_config(config_dir)
    data_dir, reports_dir = Path(data_dir), Path(reports_dir)
    now = utc_now_iso()
    run_date = now[:10]
    settings = cfg["settings"]
    client = client or HttpClient(settings.get("user_agent", "rsi-autoresearch-tracker"),
                                  timeout=settings.get("timeout", 30), retries=settings.get("retries", 3))

    prev_stats = st.load_json(data_dir / "stats.json", {})
    store = {it["id"]: it for it in st.load_jsonl(data_dir / "items.jsonl")}
    aliases = {a: it["id"] for it in store.values() for a in (it.get("extra") or {}).get("duplicate_ids") or []}
    log(f"[load] {len(store)} existing items")

    # Offline rebuilds keep the source health from the last real collection.
    health, collected = (prev_stats.get("sources") or {}) if offline else {}, []
    if not offline:
        collected, health = _collect(cfg, client, sources or set())
        attempted = [h for h in health.values() if h["status"] != "disabled"]
        if attempted and all(h["status"] == "failed" for h in attempted):
            raise PipelineError("all sources failed: " + "; ".join(e for h in attempted for e in h["errors"][:2]))
    collected = [it for it in collected if it["id"] not in aliases]

    new_ids = st.merge_items(store, collected, now)
    classifier = Classifier(cfg)
    irrelevant = [i for i, it in store.items() if not classifier.classify(it)]
    for i in irrelevant:
        del store[i]
    dropped, item_quality = quality.check_items(store)
    for msg in dropped[:20]:
        log(f"[quality] dropped {msg}")
    duplicates = st.dedupe(store)
    links = st.link_related(store)
    new_ids = [i for i in new_ids if i in store]
    log(f"[merge] collected={len(collected)} new={len(new_ids)} irrelevant={len(irrelevant)} "
        f"invalid={len(dropped)} duplicates={duplicates} links={links}")

    repo_meta, enrich_errors = {}, []
    gh_cfg = cfg["sources"].get("github") or {}
    if not offline and gh_cfg.get("enabled", True) and gh_cfg.get("enrich_curated", True) and (not sources or "github" in sources):
        repo_meta, enrich_errors = _enrich_curated(cfg, client, store)

    prev_fw = st.load_json(data_dir / "frameworks.json", [])
    prev_bench = st.load_jsonl(data_dir / "benchmarks.jsonl")
    prev_tasks = st.load_jsonl(data_dir / "benchmark_tasks.jsonl")
    frameworks = datasets.build_frameworks(cfg, store, repo_meta, prev_fw, now, classifier)
    benchmarks = datasets.build_benchmarks(cfg, store, repo_meta, prev_bench, now, classifier)
    tasks = datasets.build_benchmark_tasks(cfg, store, prev_tasks, now)

    record_errors = (quality.check_records(frameworks, "frameworks")
                     + quality.check_records(benchmarks, "benchmarks")
                     + quality.check_records(tasks, "benchmark_tasks", id_key="task_id"))
    if record_errors:
        raise PipelineError("dataset quality check failed:\n  " + "\n  ".join(record_errors[:30]))

    items = st.sort_items(store.values())
    st.write_jsonl(data_dir / "items.jsonl", items)
    st.write_json(data_dir / "frameworks.json", frameworks)
    st.write_csv(data_dir / "frameworks.csv", frameworks, datasets.FRAMEWORK_FIELDS)
    st.write_jsonl(data_dir / "benchmarks.jsonl", benchmarks)
    st.write_csv(data_dir / "benchmarks.csv", benchmarks, datasets.BENCHMARK_FIELDS)
    st.write_jsonl(data_dir / "benchmark_tasks.jsonl", tasks)

    stats = {
        "generated_at": now,
        "run_date": run_date,
        "mode": "offline-build" if offline else "collect",
        "counts": {
            "items_total": len(items),
            "new_this_run": len(new_ids),
            "new_today": sum(1 for it in items if (it.get("first_seen") or "").startswith(run_date)),
            "by_source": dict(Counter(it["source"] for it in items).most_common()),
            "by_type": dict(Counter(it["type"] for it in items).most_common()),
            "by_topic": dict(Counter(t for it in items for t in it["topics"]).most_common()),
            "by_tag": dict(Counter(t for it in items for t in it["tags"]).most_common()),
        },
        "frameworks": {"total": len(frameworks),
                       "curated": sum(r["status"] == "curated" for r in frameworks),
                       "candidates": sum(r["status"] == "candidate" for r in frameworks),
                       "by_category": dict(Counter(r["category"] for r in frameworks).most_common())},
        "benchmarks": {"total": len(benchmarks),
                       "curated": sum(r["status"] == "curated" for r in benchmarks),
                       "candidates": sum(r["status"] == "candidate" for r in benchmarks),
                       "by_focus": dict(Counter(r["focus"] for r in benchmarks).most_common())},
        "benchmark_tasks": len(tasks),
        "sources": health,
        "pipeline": {"collected": len(collected), "irrelevant_filtered": len(irrelevant),
                     "duplicates_removed": duplicates, "cross_links": links,
                     "enrich_errors": enrich_errors[:10], "http_requests": client.request_count},
        "quality": {**item_quality, "dropped_examples": dropped[:10], "record_errors": 0, "passed": True},
    }
    st.write_json(data_dir / "stats.json", stats)

    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "LATEST.md").write_text(reports.daily_report(run_date, store, stats), encoding="utf-8")
    (reports_dir / "daily").mkdir(exist_ok=True)
    (reports_dir / "daily" / f"{run_date}.md").write_text(
        reports.daily_report(run_date, store, stats, root="../../"), encoding="utf-8")
    (reports_dir / "FRAMEWORKS.md").write_text(reports.frameworks_report(frameworks, now), encoding="utf-8")
    (reports_dir / "BENCHMARKS.md").write_text(reports.benchmarks_report(benchmarks, tasks, now), encoding="utf-8")
    log(f"[done] items={len(items)} frameworks={len(frameworks)} benchmarks={len(benchmarks)} tasks={len(tasks)}")
    return stats

"""CLI: python -m tracker run|build"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .pipeline import PipelineError, run


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="tracker", description="RSI & AutoResearch 数据采集与数据集构建")
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name, help_text in (("run", "联网采集 + 构建数据集与报告"), ("build", "离线：仅用已有 data/items.jsonl 重建数据集与报告")):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--config-dir", default="config")
        p.add_argument("--data-dir", default="data")
        p.add_argument("--reports-dir", default="reports")
        if name == "run":
            p.add_argument("--sources", default="", help="逗号分隔的数据源子集，如 arxiv,github（默认全部）")
        p.add_argument("--step-summary", action="store_true", help="把日报写入 $GITHUB_STEP_SUMMARY")
    args = parser.parse_args(argv)

    sources = {s.strip() for s in getattr(args, "sources", "").split(",") if s.strip()}
    try:
        stats = run(args.config_dir, args.data_dir, args.reports_dir, sources=sources, offline=args.cmd == "build")
    except PipelineError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(json.dumps({k: stats[k] for k in ("generated_at", "counts", "frameworks", "benchmarks", "benchmark_tasks")},
                     ensure_ascii=False, indent=2))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if args.step_summary and summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(Path(args.reports_dir, "LATEST.md").read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

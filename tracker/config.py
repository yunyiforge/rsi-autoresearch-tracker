"""Load YAML config files."""
from __future__ import annotations

from pathlib import Path

import yaml


def _load(path: Path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return default if data is None else data


def load_config(config_dir: str | Path) -> dict:
    config_dir = Path(config_dir)
    cfg = _load(config_dir / "sources.yaml", {})
    cfg.setdefault("settings", {})
    cfg.setdefault("topics", {})
    cfg.setdefault("tags", {})
    cfg.setdefault("sources", {})
    cfg.setdefault("datasets", {})
    cfg["curated_frameworks"] = _load(config_dir / "frameworks.yaml", [])
    cfg["curated_benchmarks"] = _load(config_dir / "benchmarks.yaml", [])
    return cfg

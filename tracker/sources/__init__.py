"""Source collectors. Each module exposes collect(cfg, client, log) -> {"items": [...], "errors": [...]}."""
from . import arxiv, github, hn, rss

COLLECTORS = {
    "arxiv": arxiv.collect,
    "github": github.collect,
    "hn": hn.collect,
    "rss": rss.collect,
}

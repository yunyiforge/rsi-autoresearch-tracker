"""Rule-based relevance filtering, topic assignment and tagging."""
from __future__ import annotations

from .textutil import KeywordMatcher, normalize_text


class Classifier:
    def __init__(self, cfg: dict):
        self.topics = {name: KeywordMatcher((t or {}).get("keywords")) for name, t in cfg["topics"].items()}
        self.tags = {name: KeywordMatcher(kws) for name, kws in cfg.get("tags", {}).items()}
        self.exclude = KeywordMatcher(cfg.get("exclude_keywords"))
        self.sources = cfg.get("sources", {})

    @staticmethod
    def item_text(item: dict) -> str:
        parts = [item.get("title", ""), item.get("summary", "")]
        parts.extend((item.get("extra") or {}).get("topics") or [])
        return normalize_text(" ".join(p for p in parts if p))

    def classify(self, item: dict) -> bool:
        """Set topics/tags/relevance on the item; return True if it should be kept."""
        text = self.item_text(item)
        title = normalize_text(item.get("title", ""))
        rule = self.sources.get(item.get("source"), {}) or {}

        topics, score = set(), 0
        for name, matcher in self.topics.items():
            hits = matcher.find(text)
            if hits:
                topics.add(name)
                score += len(hits)
                if matcher.matches(title):
                    score += 2
        if not rule.get("require_keyword_match", False) and item.get("query_topics"):
            topics.update(t for t in item["query_topics"] if t in self.topics)
            score += 1

        tags = {name for name, m in self.tags.items() if m.matches(text)}
        if (item.get("links") or {}).get("code"):
            tags.add("has-code")

        item["topics"] = sorted(topics)
        item["tags"] = sorted(tags)
        item["relevance"] = score
        if self.exclude.matches(text):
            return False
        return bool(topics) and score >= int(rule.get("min_relevance", 1))

    def first_match(self, rules: dict, text: str, default: str = "other") -> str:
        norm = normalize_text(text)
        for name, kws in (rules or {}).items():
            if KeywordMatcher(kws).matches(norm):
                return name
        return default

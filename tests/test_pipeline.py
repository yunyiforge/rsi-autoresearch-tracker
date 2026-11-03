"""Offline tests for parsers, matching, merge/dedupe and dataset building (no network)."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tracker import datasets, quality, store as st
from tracker.classify import Classifier
from tracker.config import load_config
from tracker.pipeline import run
from tracker.sources import arxiv, github, hn, rss
from tracker.textutil import (KeywordMatcher, arxiv_id_from_url, canonical_url, find_github_repos,
                              normalize_text, to_iso)

ROOT = Path(__file__).resolve().parents[1]

ARXIV_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2505.22954v2</id>
    <updated>2025-06-01T10:00:00Z</updated>
    <published>2025-05-29T17:00:00Z</published>
    <title>Darwin Godel Machine: Open-Ended Evolution of
      Self-Improving Agents</title>
    <summary>We present a self-improving system that iteratively modifies its own code.
      Code: https://github.com/jennyzzt/dgm.</summary>
    <author><name>Jenny Zhang</name></author>
    <author><name>Jeff Clune</name></author>
    <arxiv:comment>Code at https://github.com/jennyzzt/dgm</arxiv:comment>
    <link title="pdf" href="http://arxiv.org/pdf/2505.22954v2" rel="related"/>
    <arxiv:primary_category term="cs.AI"/>
    <category term="cs.AI"/><category term="cs.LG"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2410.07095v1</id>
    <published>2024-10-09T17:00:00Z</published>
    <updated>2024-10-09T17:00:00Z</updated>
    <title>MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering</title>
    <summary>We introduce MLE-bench, a benchmark for measuring how well AI agents perform at ML engineering.</summary>
    <author><name>Jun Shern Chan</name></author>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2501.00001v1</id>
    <published>2025-01-01T00:00:00Z</published>
    <title>ResearchArena-Bench: Evaluating Research Agents on Open Problems</title>
    <summary>A new benchmark for autonomous research agents. Code: https://github.com/foo/researcharena</summary>
    <author><name>A</name></author>
  </entry>
</feed>"""

RSS_XML = b"""<?xml version="1.0"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/"><channel>
<item><title>Towards an AI Scientist&nbsp;that works</title><link>https://example.com/post?utm_source=x</link>
<description>&lt;p&gt;Notes on automated scientific discovery&lt;/p&gt;</description>
<pubDate>Mon, 02 Nov 2026 10:00:00 GMT</pubDate><dc:creator>Jack</dc:creator></item>
<item><title>Unrelated cooking post</title><link>https://example.com/food</link>
<pubDate>Mon, 02 Nov 2026 10:00:00 GMT</pubDate></item>
</channel></rss>"""

ATOM_XML = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<entry><title>Recursive self-improvement timelines</title>
<link rel="alternate" href="https://blog.example.org/rsi"/>
<published>2026-11-01T08:00:00+08:00</published><summary>On RSI.</summary>
<author><name>Ann</name></author></entry></feed>"""

GITHUB_REPO = {
    "full_name": "SakanaAI/AI-Scientist", "html_url": "https://github.com/SakanaAI/AI-Scientist",
    "description": "The AI Scientist: fully automated open-ended scientific discovery",
    "owner": {"login": "SakanaAI"}, "created_at": "2024-08-01T00:00:00Z", "pushed_at": "2026-10-01T00:00:00Z",
    "stargazers_count": 12000, "forks_count": 1700, "open_issues_count": 10, "language": "Python",
    "topics": ["ai-scientist"], "license": {"spdx_id": "Apache-2.0"}, "archived": False,
}

HN_HIT = {"objectID": "123", "title": "The Darwin Gödel Machine: AI that improves itself",
          "url": "https://arxiv.org/abs/2505.22954", "author": "pg", "points": 300,
          "num_comments": 120, "created_at_i": 1748563200}


class FakeClient:
    request_count = 0


class TextUtilTest(unittest.TestCase):
    def test_normalize_and_match(self):
        self.assertEqual(normalize_text("Self-Improving  Gödel_Machine"), "self improving godel machine")
        m = KeywordMatcher(["self improv*", "godel machine", "re:\\w*bench\\b"])
        self.assertEqual(m.find(normalize_text("A Self-Improving Gödel Machine")), ["self improv*", "godel machine"])
        self.assertTrue(m.matches(normalize_text("MLE-bench results")))
        self.assertTrue(m.matches("paperbench"))
        self.assertFalse(KeywordMatcher(["rsi"]).matches("versions"))

    def test_urls(self):
        self.assertEqual(canonical_url("http://www.Example.com/a/?utm_source=x&id=2#frag"), "https://example.com/a?id=2")
        self.assertEqual(arxiv_id_from_url("https://arxiv.org/pdf/2410.07095v3"), "2410.07095")
        self.assertEqual(find_github_repos("see https://github.com/foo/bar.git and github.com/foo/bar."), ["foo/bar"])
        self.assertEqual(find_github_repos("https://github.com/orgs/foo"), [])

    def test_dates(self):
        self.assertEqual(to_iso("Mon, 02 Nov 2026 10:00:00 GMT"), "2026-11-02T10:00:00Z")
        self.assertEqual(to_iso("2026-11-01T08:00:00+08:00"), "2026-11-01T00:00:00Z")
        self.assertEqual(to_iso(0), "1970-01-01T00:00:00Z")
        self.assertIsNone(to_iso("not a date"))


class ParserTest(unittest.TestCase):
    def test_arxiv(self):
        entries = arxiv.parse_feed(ARXIV_XML)
        self.assertEqual([e["arxiv_id"] for e in entries], ["2505.22954", "2410.07095", "2501.00001"])
        self.assertEqual(entries[0]["code_repos"], ["jennyzzt/dgm"])
        self.assertEqual(entries[0]["title"], "Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents")
        item = arxiv.entry_to_item(entries[0], "rsi")
        self.assertEqual(item["id"], "arxiv:2505.22954")
        self.assertEqual(item["links"]["code"], ["https://github.com/jennyzzt/dgm"])

    def test_arxiv_query(self):
        self.assertEqual(arxiv.build_search_query("AI scientist", ["cs.AI", "cs.LG"]),
                         '(all:"AI scientist") AND (cat:cs.AI OR cat:cs.LG)')
        self.assertEqual(arxiv.build_search_query("ti:foo", []), "ti:foo")

    def test_rss_and_atom(self):
        entries = rss.parse_feed(RSS_XML)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["summary"], "Notes on automated scientific discovery")
        self.assertEqual(entries[0]["published"], "2026-11-02T10:00:00Z")
        atom = rss.parse_feed(ATOM_XML)
        self.assertEqual(atom[0]["link"], "https://blog.example.org/rsi")
        self.assertEqual(atom[0]["author"], "Ann")
        rel = rss.parse_feed(ATOM_XML.replace(b"https://blog.example.org/rsi", b"/posts/rsi/"), base_url="https://sakana.ai/feed.xml")
        self.assertEqual(rel[0]["link"], "https://sakana.ai/posts/rsi/")

    def test_rss_fallback_and_feed_failure(self):
        from tracker.http import HttpError

        class FakeClient:
            def __init__(self):
                self.calls = []

            def get(self, url, headers=None):
                self.calls.append(url)
                if "blocked" in url:
                    raise HttpError(f"HTTP 403 for {url}", 403)
                return RSS_XML

        cfg = {"lookback_days": 100000, "feeds": [
            {"name": "Mirrored", "url": "https://blocked.example/feed",
             "fallback_urls": ["https://mirror.example/feed/"]},
            {"name": "Dead", "url": "https://blocked.example/dead"},
            {"name": "Ok", "url": "https://ok.example/feed"},
        ]}
        client, logs = FakeClient(), []
        res = rss.collect(cfg, client, logs.append)
        self.assertEqual(client.calls, ["https://blocked.example/feed", "https://mirror.example/feed/",
                                        "https://blocked.example/dead", "https://ok.example/feed"])
        self.assertEqual(len(res["items"]), 4)
        self.assertEqual({it["extra"]["feed"] for it in res["items"]}, {"Mirrored", "Ok"})
        self.assertEqual(len(res["errors"]), 1)
        self.assertIn("Dead", res["errors"][0])
        self.assertTrue(any("via https://mirror.example/feed/" in m for m in logs))

    def test_rss_full_content_excerpt(self):
        xml = b"""<?xml version="1.0"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/"><channel>
<item><title>Import AI 478: Math for alignment</title><link>https://jack-clark.net/2026/10/26/x/</link>
<description>Welcome to Import AI, a newsletter about AI research.</description>
<content:encoded><![CDATA[<p>Welcome to Import AI.</p><p>Spacecraft are cool. Labs now pursue
recursive self-improvement in earnest!</p><p>Another unrelated story.</p>]]></content:encoded>
<pubDate>Mon, 26 Oct 2026 12:31:52 +0000</pubDate></item>
</channel></rss>"""
        entry = rss.parse_feed(xml)[0]
        self.assertNotIn("_content", rss.entry_to_item(entry, "Import AI"))
        item = rss.entry_to_item(entry, "Import AI", full_content=True)
        cls = Classifier(load_config(ROOT / "config"))
        self.assertFalse(cls.classify(dict(item)))
        excerpt = cls.relevant_excerpt(item["_content"], 2000)
        self.assertEqual(excerpt, "Labs now pursue recursive self-improvement in earnest!")
        item["summary"] = excerpt
        self.assertTrue(cls.classify(item))
        self.assertIn("rsi", item["topics"])

    def test_benchmark_detection(self):
        repo = github.repo_to_item({**GITHUB_REPO, "full_name": "x/zk-autoresearch",
                                    "description": "autoresearch loop that beats a benchmark"})
        repo["tags"] = ["benchmark"]
        self.assertFalse(datasets.is_benchmark_item(repo))
        repo["summary"] = "A challenging benchmark for research agents"
        self.assertTrue(datasets.is_benchmark_item(repo))

    def test_github_and_hn(self):
        item = github.repo_to_item(GITHUB_REPO, "autoresearch")
        self.assertEqual(item["id"], "github:sakanaai/ai-scientist")
        self.assertEqual(item["metrics"]["stars"], 12000)
        h = hn.hit_to_item(HN_HIT)
        self.assertEqual(h["id"], "hn:123")
        self.assertEqual(h["links"]["discussion"], "https://news.ycombinator.com/item?id=123")


def _sample_items():
    items = [arxiv.entry_to_item(e, "rsi") for e in arxiv.parse_feed(ARXIV_XML)]
    items.append(github.repo_to_item(GITHUB_REPO, "autoresearch"))
    items.append(github.repo_to_item({**GITHUB_REPO, "full_name": "jennyzzt/dgm", "html_url": "https://github.com/jennyzzt/dgm",
                                      "description": "Darwin Godel Machine: self-improving agents", "topics": []}, "rsi"))
    items.append(hn.hit_to_item(HN_HIT))
    items.append(hn.hit_to_item({**HN_HIT, "objectID": "124", "points": 10}))
    items.extend(rss.entry_to_item(e, "Test") for e in rss.parse_feed(RSS_XML))
    return items


class PipelineLogicTest(unittest.TestCase):
    def setUp(self):
        self.cfg = load_config(ROOT / "config")
        self.clf = Classifier(self.cfg)

    def test_classify_filters(self):
        kept = {it["id"]: self.clf.classify(it) for it in _sample_items()}
        self.assertTrue(kept["arxiv:2505.22954"])
        self.assertTrue(kept["hn:123"])
        cooking = [i for i in kept if i.startswith("url:") and not kept[i]]
        self.assertEqual(len(cooking), 1)

    def test_merge_dedupe_link(self):
        store: dict = {}
        new = st.merge_items(store, _sample_items(), "2026-11-03T00:00:00Z")
        self.assertEqual(len(new), len(store))
        for i in [i for i, it in store.items() if not self.clf.classify(it)]:
            del store[i]
        dropped, _ = quality.check_items(store)
        self.assertEqual(dropped, [])
        self.assertEqual(st.dedupe(store), 1)  # hn:124 duplicates hn:123 (same URL)
        self.assertIn("hn:123", store)
        self.assertEqual(store["hn:123"]["extra"]["duplicate_ids"], ["hn:124"])
        st.link_related(store)
        self.assertIn("hn:123", store["arxiv:2505.22954"]["related_ids"])
        self.assertIn("github:jennyzzt/dgm", store["arxiv:2505.22954"]["related_ids"])
        self.assertEqual(store["arxiv:2505.22954"]["links"]["discussions"], ["https://news.ycombinator.com/item?id=123"])
        again = st.merge_items(store, [arxiv.entry_to_item(arxiv.parse_feed(ARXIV_XML)[0], "rsi")], "2026-11-04T00:00:00Z")
        self.assertEqual(again, [])
        self.assertEqual(store["arxiv:2505.22954"]["first_seen"], "2026-11-03T00:00:00Z")
        self.assertEqual(store["arxiv:2505.22954"]["last_seen"], "2026-11-04T00:00:00Z")

    def test_benchmark_name_extraction(self):
        self.assertEqual(datasets.extract_benchmark_name("MLE-bench: Evaluating ML Agents"), "MLE-bench")
        self.assertEqual(datasets.extract_benchmark_name("Evaluating agents with the new PaperBench suite"), "PaperBench")

    def test_datasets(self):
        store: dict = {}
        st.merge_items(store, _sample_items(), "2026-11-03T00:00:00Z")
        for i in [i for i, it in store.items() if not self.clf.classify(it)]:
            del store[i]
        now = "2026-11-03T00:00:00Z"
        fws = datasets.build_frameworks(self.cfg, store, {}, [], now, self.clf)
        benches = datasets.build_benchmarks(self.cfg, store, {}, [], now, self.clf)
        tasks = datasets.build_benchmark_tasks(self.cfg, store, [], now)
        self.assertEqual(quality.check_records(fws, "frameworks"), [])
        self.assertEqual(quality.check_records(benches, "benchmarks"), [])
        dgm = next(r for r in fws if r["repo"] == "jennyzzt/dgm")
        self.assertEqual(dgm["stars"], 12000)  # taken from the collected github item
        self.assertIn("arxiv:2505.22954", dgm["evidence"])
        mle = next(r for r in benches if r["name"] == "MLE-bench")
        self.assertEqual(mle["status"], "curated")
        self.assertIn("arxiv:2410.07095", mle["evidence"])
        cand = [r for r in benches if r["status"] == "candidate"]
        self.assertEqual([r["name"] for r in cand], ["ResearchArena-Bench"])
        self.assertEqual(cand[0]["repo"], "foo/researcharena")
        self.assertEqual({t["task_id"] for t in tasks}, {"replicate:2505.22954", "replicate:2501.00001"})


class OfflineBuildTest(unittest.TestCase):
    def test_build_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            data, reports = Path(tmp, "data"), Path(tmp, "reports")
            store: dict = {}
            st.merge_items(store, _sample_items(), "2026-11-03T00:00:00Z")
            st.write_jsonl(data / "items.jsonl", list(store.values()))
            stats = run(ROOT / "config", data, reports, offline=True, client=FakeClient())
            self.assertTrue(stats["quality"]["passed"])
            self.assertGreater(stats["counts"]["items_total"], 4)
            for f in ("items.jsonl", "frameworks.json", "frameworks.csv", "benchmarks.jsonl",
                      "benchmarks.csv", "benchmark_tasks.jsonl", "stats.json"):
                self.assertTrue((data / f).exists(), f)
            for f in ("LATEST.md", "FRAMEWORKS.md", "BENCHMARKS.md"):
                self.assertTrue((reports / f).read_text(encoding="utf-8").startswith("# "), f)
            rows = [json.loads(line) for line in (data / "items.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(rows), len({r["id"] for r in rows}))


if __name__ == "__main__":
    unittest.main()

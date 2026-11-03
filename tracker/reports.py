"""Markdown report generation."""
from __future__ import annotations

from collections import Counter

TOPIC_LABEL = {"rsi": "RSI", "autoresearch": "AutoResearch"}


def _cell(text) -> str:
    if text is None:
        return ""
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def _badges(item: dict) -> str:
    topics = " ".join(f"`{TOPIC_LABEL.get(t, t)}`" for t in item.get("topics", []))
    tags = " ".join(f"`#{t}`" for t in item.get("tags", [])[:5])
    return f"{topics} {tags}".strip()


def _link(name, url) -> str:
    return f"[{_cell(name)}]({url})" if url else _cell(name)


def _stars(n) -> str:
    return "" if n is None else f"{int(n):,}"


def _paper_lines(items, limit) -> list[str]:
    out = []
    for it in items[:limit]:
        authors = it.get("authors") or []
        who = (authors[0] + (" et al." if len(authors) > 1 else "")) if authors else ""
        code = " · 💻 code" if (it.get("links") or {}).get("code") else ""
        out.append(f"- {_link(it['title'], it['url'])} — {who} · {(it.get('published') or '')[:10]}{code} {_badges(it)}")
    return out


def daily_report(run_date: str, store: dict, stats: dict, root: str = "../") -> str:
    """root: relative path from the report file to the repository root."""
    today = [it for it in store.values() if (it.get("first_seen") or "").startswith(run_date)]
    by_type = {t: sorted([i for i in today if i["type"] == t], key=lambda i: -i.get("relevance", 0))
               for t in ("paper", "repo", "discussion", "article")}
    c = stats["counts"]
    lines = [
        f"# RSI & AutoResearch 每日追踪 · {run_date}",
        "",
        f"> 自动生成于 {stats['generated_at']}（UTC）。累计 **{c['items_total']}** 条数据，"
        f"今日新增 **{len(today)}** 条；框架 {stats['frameworks']['total']} 个，"
        f"benchmark {stats['benchmarks']['total']} 个，复现任务候选 {stats['benchmark_tasks']} 个。",
        "",
        "## 运行概况",
        "",
        "| 数据源 | 状态 | 本次抓取 | 错误 |",
        "|---|---|---:|---|",
    ]
    for name, h in stats["sources"].items():
        err = _cell("; ".join(h.get("errors") or [])[:160])
        lines.append(f"| {name} | {h.get('status')} | {h.get('fetched', 0)} | {err} |")

    lines += ["", f"## 🆕 新论文（{len(by_type['paper'])}）", ""]
    lines += _paper_lines(by_type["paper"], 40) or ["_今日无新增_"]

    lines += ["", f"## 🆕 新仓库（{len(by_type['repo'])}）", ""]
    repos = sorted(by_type["repo"], key=lambda i: -int((i.get("metrics") or {}).get("stars") or 0))
    if repos:
        lines += ["| 仓库 | ⭐ | 描述 | 标签 |", "|---|---:|---|---|"]
        for it in repos[:40]:
            lines.append(f"| {_link(it['title'], it['url'])} | {_stars((it.get('metrics') or {}).get('stars'))} | "
                         f"{_cell(it.get('summary', ''))[:140]} | {_badges(it)} |")
    else:
        lines.append("_今日无新增_")

    news = sorted(by_type["discussion"] + by_type["article"], key=lambda i: i.get("published") or "", reverse=True)
    lines += ["", f"## 🆕 讨论与博客（{len(news)}）", ""]
    for it in news[:40]:
        src = "HN" if it["source"] == "hn" else (it.get("extra") or {}).get("feed", "Blog")
        pts = (it.get("metrics") or {}).get("points")
        extra = f" · ▲{pts}" if pts else ""
        disc = (it.get("links") or {}).get("discussion")
        disc_link = f" · [讨论]({disc})" if disc and disc != it["url"] else ""
        lines.append(f"- **{_cell(src)}** {_link(it['title'], it['url'])}{extra}{disc_link} {_badges(it)}")
    if not news:
        lines.append("_今日无新增_")

    top = sorted((i for i in store.values() if i["source"] == "github"),
                 key=lambda i: -int((i.get("metrics") or {}).get("stars") or 0))[:15]
    lines += ["", "## 🔥 Star 最多的相关仓库（累计）", "", "| 仓库 | ⭐ | 主题 |", "|---|---:|---|"]
    for it in top:
        lines.append(f"| {_link(it['title'], it['url'])} | {_stars((it.get('metrics') or {}).get('stars'))} | {_badges(it)} |")

    lines += ["", "---", "", f"完整数据：[`data/items.jsonl`]({root}data/items.jsonl) · "
              f"[框架]({root}reports/FRAMEWORKS.md) · [Benchmark]({root}reports/BENCHMARKS.md) · [统计]({root}data/stats.json)", ""]
    return "\n".join(lines)


def frameworks_report(records: list[dict], generated_at: str) -> str:
    curated = [r for r in records if r["status"] == "curated"]
    cands = [r for r in records if r["status"] == "candidate"]
    lines = [
        "# RSI & AutoResearch 技术框架清单",
        "",
        f"> 自动生成于 {generated_at}（UTC）。精选 {len(curated)} 个（`config/frameworks.yaml`）+ "
        f"自动发现候选 {len(cands)} 个。Star 数据每日刷新。",
        "",
    ]
    for cat in sorted({r["category"] for r in curated}):
        rows = sorted([r for r in curated if r["category"] == cat], key=lambda r: -(r.get("stars") or 0))
        lines += [f"## {cat}", "", "| 框架 | 机构 | ⭐ | 最近提交 | 论文 | 说明 |", "|---|---|---:|---|---|---|"]
        for r in rows:
            paper = f"[arXiv](https://arxiv.org/abs/{r['arxiv_id']})" if r.get("arxiv_id") else ""
            status = " ⚠️" if r.get("repo_status") in ("not_found", "archived") else ""
            lines.append(f"| {_link(r['name'], r.get('url'))}{status} | {_cell(r.get('org'))} | {_stars(r.get('stars'))} | "
                         f"{(r.get('last_push') or '')[:10]} | {paper} | {_cell(r.get('description'))} |")
        lines.append("")
    lines += ["## 自动发现的候选（待人工审核）", "",
              "按 star 排序；审核通过后可移入 `config/frameworks.yaml`。", "",
              "| 仓库 | 类别 | ⭐ | 主题 | 描述 |", "|---|---|---:|---|---|"]
    for r in cands:
        topics = " ".join(f"`{TOPIC_LABEL.get(t, t)}`" for t in r.get("topics", []))
        lines.append(f"| {_link(r['repo'], r.get('url'))} | {r['category']} | {_stars(r.get('stars'))} | {topics} | "
                     f"{_cell(r.get('description'))[:140]} |")
    return "\n".join(lines) + "\n"


def benchmarks_report(records: list[dict], tasks: list[dict], generated_at: str) -> str:
    curated = [r for r in records if r["status"] == "curated"]
    cands = [r for r in records if r["status"] == "candidate"]
    lines = [
        "# RSI & AutoResearch Benchmark 数据集",
        "",
        f"> 自动生成于 {generated_at}（UTC）。精选 {len(curated)} 个 + 自动发现候选 {len(cands)} 个；"
        f"论文复现任务候选 {len(tasks)} 个。构建方法见 [docs/BENCHMARK_PIPELINE.md](../docs/BENCHMARK_PIPELINE.md)。",
        "",
        "## 精选 Benchmark",
        "",
        "| Benchmark | 方向 | 机构 | 年份 | 规模 | 指标 | 论文 | ⭐ |",
        "|---|---|---|---|---|---|---|---:|",
    ]
    for r in sorted(curated, key=lambda r: (r["focus"], r["name"])):
        paper = _link("arXiv", r.get("paper_url")) if r.get("paper_url") else ""
        name = _link(r["name"], f"https://github.com/{r['repo']}" if r.get("repo") else r.get("homepage") or r.get("paper_url"))
        lines.append(f"| {name} | {r['focus']} | {_cell(r.get('org'))} | {r.get('year') or ''} | {_cell(r.get('tasks'))} | "
                     f"{_cell(r.get('metric'))} | {paper} | {_stars(r.get('stars'))} |")

    focus_counts = Counter(r["focus"] for r in cands)
    lines += ["", "## 自动发现的 Benchmark 候选", "",
              "按方向统计：" + ("，".join(f"{k} {v}" for k, v in focus_counts.most_common()) or "暂无"), "",
              "| 名称 | 方向 | 年份 | 论文 | 仓库 | 首次发现 |", "|---|---|---|---|---|---|"]
    for r in cands:
        paper = _link("arXiv", r.get("paper_url")) if r.get("paper_url") else ""
        repo = _link(r["repo"], f"https://github.com/{r['repo']}") if r.get("repo") else ""
        lines.append(f"| {_cell(r['name'])} | {r['focus']} | {r.get('year') or ''} | {paper} | {repo} | {(r.get('first_seen') or '')[:10]} |")

    diff = Counter(t["difficulty_hint"] for t in tasks)
    lines += ["", "## 论文复现任务候选（自动构建）", "",
              f"共 {len(tasks)} 个（难度提示：" + "，".join(f"{k} {v}" for k, v in sorted(diff.items())) +
              "）。完整数据见 [`data/benchmark_tasks.jsonl`](../data/benchmark_tasks.jsonl)。", "",
              "| 任务 | 论文 | 官方代码 | 难度 |", "|---|---|---|---|"]
    for t in tasks[:30]:
        code = ", ".join(f"[{u.split('github.com/')[-1]}]({u})" for u in t["code_repos"][:2])
        lines.append(f"| `{t['task_id']}` | {_link(t['paper']['title'], t['paper']['url'])} | {code} | {t['difficulty_hint']} |")
    return "\n".join(lines) + "\n"

# rsi-autoresearch-tracker

[![Collect RSI & AutoResearch data](https://github.com/yunyiforge/rsi-autoresearch-tracker/actions/workflows/collect.yml/badge.svg)](https://github.com/yunyiforge/rsi-autoresearch-tracker/actions/workflows/collect.yml)

每天由 GitHub Actions 自动采集 **RSI（Recursive Self-Improvement，递归自我改进）** 与
**AutoResearch（AI 自动科研）** 相关的论文、开源仓库、社区讨论和博客，并自动构建：

- 📚 **条目库**：去重、分类、打标签后的论文 / 仓库 / 讨论 / 博文；
- 🧰 **技术框架清单**：人工精选（autoresearch、AI Scientist、Darwin Gödel Machine、OpenEvolve、DSPy 等）+ 自动发现的候选；
- 📏 **Benchmark 目录**：人工精选（MLE-bench、RE-Bench、PaperBench、MLAgentBench、CORE-Bench 等）+ 自动发现的候选；
- 🧪 **论文复现任务候选集**：PaperBench 风格，从「相关论文 + 官方代码」自动生成。

🌐 **网站：<https://yunyiforge.github.io/rsi-autoresearch-tracker/>** —— 可搜索、筛选条目 / 框架 / Benchmark / 复现任务并阅读日报，随每日 Action 自动更新。

## 快速查看

| 内容 | 链接 |
| --- | --- |
| 🌐 网站（搜索 / 筛选） | <https://yunyiforge.github.io/rsi-autoresearch-tracker/> |
| 今日日报 | [reports/LATEST.md](reports/LATEST.md)（历史：[reports/daily/](reports/daily/)） |
| 技术框架清单 | [reports/FRAMEWORKS.md](reports/FRAMEWORKS.md) · [JSON](data/frameworks.json) · [CSV](data/frameworks.csv) |
| Benchmark 清单 | [reports/BENCHMARKS.md](reports/BENCHMARKS.md) · [JSONL](data/benchmarks.jsonl) · [CSV](data/benchmarks.csv) |
| 复现任务候选 | [data/benchmark_tasks.jsonl](data/benchmark_tasks.jsonl) |
| 全部条目 | [data/items.jsonl](data/items.jsonl) |
| 统计 / 数据源健康 | [data/stats.json](data/stats.json) |
| 数据构建方法 | [docs/BENCHMARK_PIPELINE.md](docs/BENCHMARK_PIPELINE.md) |

## 数据来源

| 数据源 | 接口 | 是否需要 key |
| --- | --- | --- |
| arXiv | arXiv API（cs.AI / LG / CL / MA / NE / SE） | 否 |
| GitHub | Search API + Repos API | Actions 自带 `GITHUB_TOKEN` |
| Hacker News | Algolia HN Search API | 否 |
| 博客 | RSS / Atom（Import AI、Interconnects、DeepMind、OpenAI、Sakana AI、METR 等） | 否 |

## 目录结构

```
.github/workflows/collect.yml  每日定时 / 手动触发的采集 workflow（结束后部署网站）
.github/workflows/pages.yml    GitHub Pages 部署（可复用 workflow）
config/
  sources.yaml                 关键词、主题、标签、数据源查询、数据集构建规则
  frameworks.yaml              精选技术框架
  benchmarks.yaml              精选 benchmark
tracker/                       Python 包（仅依赖标准库 + PyYAML）
  sources/                     arxiv / github / hn / rss 采集器
  classify.py                  关键词匹配、主题打分、打标签
  store.py                     增量合并、去重、关联、读写
  datasets.py                  frameworks / benchmarks / benchmark_tasks 构建
  quality.py                   schema 与一致性检查
  reports.py                   Markdown 报告
  pipeline.py                  流水线编排
tests/                         离线单元测试
site/                          GitHub Pages 静态网站（index.html + assets/，build.sh 组装 _site/）
data/                          生成的数据（由 Action 自动提交）
reports/                       生成的报告（由 Action 自动提交）
docs/BENCHMARK_PIPELINE.md     Benchmark 数据自动化构建方法说明
```

## 本地运行

```bash
pip install -r requirements.txt

# 联网采集 + 构建（建议提供 token，GitHub 限额更高）
GITHUB_TOKEN=$(gh auth token) python -m tracker run

# 只采集部分数据源
python -m tracker run --sources arxiv,hn

# 不联网：用已有 data/items.jsonl 按当前配置重建数据集和报告（调规则时很有用）
python -m tracker build

# 测试
python -m unittest discover -s tests
```

完整采集约 5–6 分钟（arXiv 要求请求间隔 ≥ 3 秒）。运行日志输出到 stderr，统计 JSON 输出到 stdout。

## GitHub Action

`.github/workflows/collect.yml`：

- **触发**：每天 01:17 UTC（北京时间 09:17）；Actions 页面手动 *Run workflow*（可填 `sources` 只跑部分数据源）；修改 `tracker/`、`config/` 后推送到 main 也会触发。
- **步骤**：安装依赖 → 单元测试 → 采集与构建（结果写入 Step Summary）→ 有变化时以 `github-actions[bot]` 提交 `data/` 与 `reports/`。
- **权限**：`contents: write`；只使用内置 `GITHUB_TOKEN`，无需配置额外 secret。
- 质量检查失败时运行失败，不会提交数据。
- **网站部署**：采集成功后以 `workflow_call` 调用 `.github/workflows/pages.yml`，用 `site/build.sh` 把 `site/`（无构建工具的静态页面）与最新的 `data/`、`reports/` 组装后发布到 GitHub Pages（需要 `pages: write`、`id-token: write`）。修改 `site/` 后推送到 main 或手动运行 `pages.yml` 也会重新部署。本地预览：`./site/build.sh && python -m http.server -d _site 8000`。

## 数据结构（摘要）

`data/items.jsonl` 每行一个条目：

```json
{
  "id": "arxiv:2410.07095",
  "source": "arxiv", "type": "paper",
  "title": "...", "url": "https://arxiv.org/abs/2410.07095", "summary": "...",
  "authors": ["..."], "published": "2024-10-09T...Z", "updated": "...",
  "first_seen": "...", "last_seen": "...",
  "topics": ["autoresearch"], "relevance": 5,
  "tags": ["benchmark", "ml-engineering", "has-code"],
  "metrics": {}, "links": {"pdf": "...", "discussions": ["..."]},
  "related_ids": ["github:openai/mle-bench"], "extra": {"code_repos": ["..."]}, "query_topics": ["autoresearch"]
}
```

- `source/type`：`arxiv/paper`、`github/repo`、`hn/discussion`、`rss/article`
- `topics`：`rsi`、`autoresearch`；`tags`：`benchmark`、`framework`、`survey`、`dataset`、`safety`、`evolutionary-search`、`code-agent`、`ml-engineering`、`paper-replication`、`idea-generation`、`prompt-optimization`、`self-training`、`multi-agent`、`science-domain`、`has-code`
- 框架、benchmark、复现任务的完整字段见 [docs/BENCHMARK_PIPELINE.md](docs/BENCHMARK_PIPELINE.md#6-schema)。

## 调整采集范围

只需改配置，无需改代码：

- 关键词 / 主题：`config/sources.yaml → topics`（支持整词、`前缀*`、`re:正则`）
- 排除噪声：`exclude_keywords`、`datasets.frameworks.exclude_keywords`
- 查询与博客：`sources.<arxiv|github|hn|rss>`（RSS feed 可配 `fallback_urls` 备用地址、`full_content: true` 用全文命中句做摘要；单个 feed 失败只记警告，不会让 workflow 失败）
- 标签、框架类别、benchmark 领域：`tags`、`datasets.*`
- 精选清单：`config/frameworks.yaml`、`config/benchmarks.yaml`

改完后可先 `python -m tracker build` 离线看效果，再推送到 main（会自动触发一次采集）。

# RSI & AutoResearch 技术框架清单

> 自动生成于 2026-11-08T07:22:23Z（UTC）。精选 32 个（`config/frameworks.yaml`）+ 自动发现候选 80 个。Star 数据每日刷新。

## agent-infra

| 框架 | 机构 | ⭐ | 最近提交 | 论文 | 说明 |
|---|---|---:|---|---|---|
| [OpenHands](https://github.com/All-Hands-AI/OpenHands) |  | 92,919 | 2026-11-08 |  | 开源软件工程 agent 平台，常作为自我改进编码循环的执行器 |
| [MetaGPT](https://github.com/geekan/MetaGPT) |  | 71,216 | 2026-01-21 |  | 多 agent 协作框架，含 Data Interpreter 等数据科学 agent |
| [AutoGen](https://github.com/microsoft/autogen) | Microsoft | 61,745 | 2026-10-28 |  | 多 agent 对话与编排框架 |
| [smolagents](https://github.com/huggingface/smolagents) | Hugging Face | 30,262 | 2026-11-03 |  | 轻量级 code-agent 框架，官方含 open deep research 示例 |
| [SWE-agent](https://github.com/SWE-agent/SWE-agent) | Princeton / Stanford | 20,755 | 2026-11-02 |  | 面向真实仓库修复的编码 agent 与 agent-computer interface |

## autoresearch-system

| 框架 | 机构 | ⭐ | 最近提交 | 论文 | 说明 |
|---|---|---:|---|---|---|
| [autoresearch](https://github.com/karpathy/autoresearch) | Andrej Karpathy | 99,497 | 2026-03-26 |  | 让 AI agent 在单 GPU 上自主修改训练代码、跑实验、保留改进的极简自动科研循环 |
| [RD-Agent](https://github.com/microsoft/RD-Agent) | Microsoft | 15,281 | 2026-10-21 |  | 面向数据驱动研发（量化、Kaggle、模型研发）的自动 R&D agent 框架 |
| [The AI Scientist](https://github.com/SakanaAI/AI-Scientist) | Sakana AI | 14,961 | 2025-12-19 | [arXiv](https://arxiv.org/abs/2408.06292) | 从想法生成、写代码做实验到撰写论文与自动评审的全自动科研流水线 |
| [PaperQA2](https://github.com/Future-House/paper-qa) | FutureHouse | 9,564 | 2026-10-26 | [arXiv](https://arxiv.org/abs/2409.13740) | 面向科学文献的高精度 RAG / 文献综述 agent |
| [The AI Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) | Sakana AI | 7,475 | 2025-12-19 | [arXiv](https://arxiv.org/abs/2504.08066) | 基于 agentic tree search 的第二代 AI Scientist，产出过通过 workshop 评审的论文 |
| [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | AMD / JHU | 5,925 | 2025-08-20 | [arXiv](https://arxiv.org/abs/2501.04227) | 文献综述→实验→报告撰写的多 agent 科研助手，支持人类在环 |
| [AI-Researcher](https://github.com/HKUDS/AI-Researcher) | HKU Data Intelligence Lab | 5,876 | 2025-10-16 |  | 端到端自动化科研框架，覆盖文献、想法、实现、实验与论文写作 |
| [data-to-paper](https://github.com/Technion-Kishony-lab/data-to-paper) | Technion | 834 | 2025-07-19 |  | 从数据出发、可追溯地自动完成假设→分析→论文写作的科研流程 |

## deep-research

| 框架 | 机构 | ⭐ | 最近提交 | 论文 | 说明 |
|---|---|---:|---|---|---|
| [STORM](https://github.com/stanford-oval/storm) | Stanford OVAL | 31,826 | 2025-09-30 | [arXiv](https://arxiv.org/abs/2402.14207) | 多视角提问 + 检索，自动生成维基百科式长篇研究报告 |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) |  | 30,550 | 2026-10-10 |  | 开源自主研究 agent，自动检索并生成带引用的研究报告 |
| [deep-research](https://github.com/dzhng/deep-research) |  | 19,878 | 2026-04-11 |  | 极简的迭代式深度研究 agent 实现 |
| [Open Deep Research](https://github.com/langchain-ai/open_deep_research) ⚠️ | LangChain | 12,675 | 2026-08-10 |  | 可配置的开源 deep research agent 参考实现 |

## evolutionary-search

| 框架 | 机构 | ⭐ | 最近提交 | 论文 | 说明 |
|---|---|---:|---|---|---|
| [OpenEvolve](https://github.com/codelion/openevolve) |  | 7,733 | 2026-11-07 |  | AlphaEvolve 的开源实现，LLM 驱动的程序进化框架 |
| [ShinkaEvolve](https://github.com/SakanaAI/ShinkaEvolve) | Sakana AI | 1,502 | 2026-10-05 |  | 样本高效的 LLM 程序进化框架，面向开放式科学发现 |
| [FunSearch](https://github.com/google-deepmind/funsearch) | Google DeepMind | 1,144 | 2024-02-05 |  | LLM + 进化搜索在数学问题上发现新构造的方法 |
| [AlphaEvolve](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) | Google DeepMind |  |  | [arXiv](https://arxiv.org/abs/2506.13131) | Gemini 驱动的进化式编码 agent，用于算法与数学发现（未开源） |

## ml-engineering-agent

| 框架 | 机构 | ⭐ | 最近提交 | 论文 | 说明 |
|---|---|---:|---|---|---|
| [AIDE](https://github.com/WecoAI/aideml) | Weco AI | 1,618 | 2026-10-16 | [arXiv](https://arxiv.org/abs/2502.13138) | 在代码空间做树搜索的 ML 工程 agent，MLE-bench 上的主力基线 |

## prompt-program-optimization

| 框架 | 机构 | ⭐ | 最近提交 | 论文 | 说明 |
|---|---|---:|---|---|---|
| [DSPy](https://github.com/stanfordnlp/dspy) | Stanford NLP | 38,969 | 2026-11-07 | [arXiv](https://arxiv.org/abs/2310.03714) | 声明式 LM 程序与自动 prompt/权重优化框架 |
| [GEPA](https://github.com/gepa-ai/gepa) |  | 7,333 | 2026-11-07 | [arXiv](https://arxiv.org/abs/2507.19457) | 基于反思与 Pareto 进化的 prompt 优化器 |
| [TextGrad](https://github.com/zou-group/textgrad) | Stanford | 3,786 | 2025-07-25 | [arXiv](https://arxiv.org/abs/2406.07496) | 用文本“梯度”反向传播优化复合 AI 系统 |
| [GPTSwarm](https://github.com/metauto-ai/GPTSwarm) |  | 1,068 | 2026-02-05 | [arXiv](https://arxiv.org/abs/2402.16823) | 把 agent 建模为可优化计算图，自动优化节点 prompt 与连接 |

## self-improvement

| 框架 | 机构 | ⭐ | 最近提交 | 论文 | 说明 |
|---|---|---:|---|---|---|
| [Voyager](https://github.com/MineDojo/Voyager) | NVIDIA / Caltech | 7,318 | 2024-04-03 | [arXiv](https://arxiv.org/abs/2305.16291) | 通过自动课程与技能库持续自我扩展能力的终身学习 agent |
| [Darwin Gödel Machine](https://github.com/jennyzzt/dgm) | Sakana AI / UBC | 2,490 | 2025-08-13 | [arXiv](https://arxiv.org/abs/2505.22954) | 通过开放式进化不断改写自身代码的自我改进编码 agent |
| [ADAS (Meta Agent Search)](https://github.com/ShengranHu/ADAS) | UBC / Vector Institute | 1,661 | 2025-01-28 | [arXiv](https://arxiv.org/abs/2408.08435) | 用 meta agent 自动设计、迭代新的 agent 系统（Automated Design of Agentic Systems） |
| [Self-Improving Coding Agent (SICA)](https://github.com/MaximeRobeyns/self_improving_coding_agent) | University of Bristol | 415 | 2025-04-23 | [arXiv](https://arxiv.org/abs/2504.15228) | 能编辑自身代码库以提升基准成绩的编码 agent |
| [Gödel Agent](https://github.com/Arvid-pku/Godel_Agent) |  | 240 | 2025-09-17 | [arXiv](https://arxiv.org/abs/2410.04444) | 受 Gödel machine 启发、可递归修改自身逻辑的自指 agent 框架 |
| [STOP (Self-Taught Optimizer)](https://github.com/microsoft/stop) | Microsoft Research | 58 | 2024-01-01 | [arXiv](https://arxiv.org/abs/2310.02304) | 递归改进“改进器”代码本身的自我优化脚手架 |

## 自动发现的候选（待人工审核）

按 star 排序；审核通过后可移入 `config/frameworks.yaml`。

| 仓库 | 类别 | ⭐ | 主题 | 描述 |
|---|---|---:|---|---|
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | autoresearch-system | 56,431 | `AutoResearch` | Turn any AI agent into an AI Scientist. The #1 Agent Skills library for science, used by 250,000+ scientists worldwide. 177 ready-to-use val |
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | self-improvement | 41,763 | `RSI` | Self-evolving Context Database for AI Agents. Unify Agent Memory, Knowledge RAG and Skills. |
| [letta-ai/letta](https://github.com/letta-ai/letta) | self-improvement | 25,383 | `RSI` | Platform for stateful agents: AI with advanced memory that can learn and self-improve over time. |
| [PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent) | self-improvement | 22,616 | `RSI` | A self-improving RLM agent for coding workflows and long-running autonomous tasks. |
| [Alibaba-NLP/DeepResearch](https://github.com/Alibaba-NLP/DeepResearch) | autoresearch-system | 20,110 | `AutoResearch` | Tongyi Deep Research, the Leading Open-source Deep Research Agent |
| [aiming-lab/AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw) | self-improvement | 14,836 | `AutoResearch` `RSI` | Fully autonomous & self-evolving research from idea to paper. Chat an Idea. Get a Paper. 🦞 |
| [lsdefine/GenericAgent](https://github.com/lsdefine/GenericAgent) | self-improvement | 14,396 | `RSI` | Self-evolving agent: grows skill tree from 3.3K-line seed, achieving full system control with 6x less token consumption |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | autoresearch-system | 14,346 | `AutoResearch` | Comprehensive open-source library of AI research and engineering skills for any AI model. Package the skills and your claude code/codex/gemi |
| [EverMind-AI/EverOS](https://github.com/EverMind-AI/EverOS) | self-improvement | 13,849 | `RSI` | One portable memory layer for every AI agent: local-first, Markdown-native, user-owned, and self-evolving across apps, tools, and workflows. |
| [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | self-improvement | 12,316 | `RSI` | Self-evolving memory OS for LLM & AI Agents: ultra-persistent memory, hybrid-retrieval, and cross-task skill reuse, with 35.24% token saving |
| [aden-hive/hive](https://github.com/aden-hive/hive) | agent-infra | 11,145 | `RSI` | Multi-Agent Harness for Production AI |
| [Companion-Inc/feynman](https://github.com/Companion-Inc/feynman) | autoresearch-system | 10,087 | `AutoResearch` | The open source AI research agent. |
| [MervinPraison/PraisonAI](https://github.com/MervinPraison/PraisonAI) | self-improvement | 9,322 | `RSI` | PraisonAI 🦞 — Hire a 24/7 AI Workforce. Stop writing boilerplate and start shipping autonomous self-improving agents that research, plan, co |
| [EvoMap/evolver](https://github.com/EvoMap/evolver) | self-improvement | 8,724 | `RSI` | The GEP-powered self-evolving engine for AI agents. Auditable evolution with Genes, Capsules, and Events. \| evomap.ai |
| [davebcn87/pi-autoresearch](https://github.com/davebcn87/pi-autoresearch) | autoresearch-system | 8,223 | `AutoResearch` | Autonomous experiment loop extension for pi |
| [alphaXiv/OpenResearch](https://github.com/alphaXiv/OpenResearch) | autoresearch-system | 7,979 | `AutoResearch` | Turn your coding agents into research agents |
| [Human-Agent-Society/reef](https://github.com/Human-Agent-Society/reef) | self-improvement | 7,785 | `RSI` | Infrastructure for continually self‑improving agents |
| [dwzhu-pku/PaperBanana](https://github.com/dwzhu-pku/PaperBanana) | autoresearch-system | 7,591 | `AutoResearch` | PaperBanana: Automating Academic Illustration For AI Scientists |
| [alchaincyf/darwin-skill](https://github.com/alchaincyf/darwin-skill) | autoresearch-system | 6,837 | `AutoResearch` `RSI` | 达尔文.skill —— 一个让你的Skill无限进化的系统：评估→改进→测试→保留或回滚 \| Autoresearch-inspired autonomous skill optimization for Claude Code. Evaluate, improve, tes |
| [uditgoenka/autoresearch](https://github.com/uditgoenka/autoresearch) | autoresearch-system | 6,813 | `AutoResearch` | Claude Autoresearch Skill — Autonomous goal-directed iteration for Claude Code. Inspired by Karpathy's autoresearch. Modify → Verify → Keep/ |
| [EverMind-AI/Raven](https://github.com/EverMind-AI/Raven) | self-improvement | 6,104 | `RSI` | The Harness of Harnesses • Super Agent: a trusted, persistent, self-evolving multi-agent ecosystem for all-domain collaboration. |
| [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | autoresearch-system | 6,015 | `AutoResearch` | Semi-automated research assistant for academic research and software development. Supports Claude Code, Codex CLI, Kimi Code CLI, and OpenCo |
| [aiwaves-cn/agents](https://github.com/aiwaves-cn/agents) | self-improvement | 5,965 | `RSI` | An Open-source Framework for Data-centric, Self-evolving Autonomous Language Agents |
| [EvoScientist/EvoScientist](https://github.com/EvoScientist/EvoScientist) | autoresearch-system | 4,938 | `AutoResearch` `RSI` | 🔬 Harness Vibe Research with Self-evolving AI Scientists |
| [ruc-datalab/DeepAnalyze](https://github.com/ruc-datalab/DeepAnalyze) | agent-infra | 4,794 | `AutoResearch` | DeepAnalyze is the first agentic LLM for autonomous data science. 🎈你的AI数据分析师，自动分析大量数据，一键生成专业分析报告！ |
| [jordan-gibbs/hyperresearch](https://github.com/jordan-gibbs/hyperresearch) | autoresearch-system | 4,437 | `AutoResearch` | Convert Claude Code or Codex into the most intelligent Deep Research Agent. Collect, search, and synthesize web research into a persistent,  |
| [letta-ai/letta-code](https://github.com/letta-ai/letta-code) | self-improvement | 3,800 | `RSI` | Agents that self-improve with experience |
| [yilewang/llm-for-zotero](https://github.com/yilewang/llm-for-zotero) | autoresearch-system | 3,520 | `AutoResearch` | An open-source research agent system for your Zotero library. |
| [ANative-Lab/EvoAgentX](https://github.com/ANative-Lab/EvoAgentX) | self-improvement | 3,424 | `RSI` | 🚀 EvoAgentX: Building a Self-Evolving Ecosystem of AI Agents |
| [Asymptote-Labs/agent-beacon](https://github.com/Asymptote-Labs/agent-beacon) | self-improvement | 3,383 | `RSI` | The cross-harness, self-improving memory layer for AI agents. Join our community: https://discord.com/invite/zdNChS2fBu |
| [sentrux/sentrux](https://github.com/sentrux/sentrux) | self-improvement | 3,340 | `RSI` | Real-time architectural sensor that helps AI agents close the feedback loop, enabling recursive self-improvement of code quality. Pure Rust. |
| [neomjs/neo](https://github.com/neomjs/neo) | self-improvement | 3,299 | `RSI` | Neo.mjs is a self-evolving software organism: a professional end-to-end AI engineering team whose cross-model swarm inhabits live apps via N |
| [Prism-Shadow/penguin-harness](https://github.com/Prism-Shadow/penguin-harness) | other | 3,187 | `RSI` | 🐧 Unified and Stable RSI Platform |
| [leo-lilinxiao/codex-autoresearch](https://github.com/leo-lilinxiao/codex-autoresearch) | autoresearch-system | 3,149 | `AutoResearch` | Codex Autoresearch Skill — A self-directed iterative system for Codex that continuously cycles through: modify, verify, retain or discard, a |
| [EvoMap/AutoResearch](https://github.com/EvoMap/AutoResearch) | autoresearch-system | 3,092 | `AutoResearch` | AI/ML research agents from idea to paper-ready evidence. An EvoMap open-source project. |
| [OpenNSWM-Lab/FAROS](https://github.com/OpenNSWM-Lab/FAROS) | autoresearch-system | 3,042 | `AutoResearch` | A blueprint-driven AutoResearch runtime for orchestrating AI research workflows from idea generation and experiments to paper writing and pe |
| [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) | other | 3,018 | `AutoResearch` | MCP, CLI, Skills for searching and downloading academic papers from multiple sources like arXiv, PubMed, bioRxiv, etc. |
| [PhyAgentOS/PhyAgentOS-core](https://github.com/PhyAgentOS/PhyAgentOS-core) | self-improvement | 2,995 | `RSI` | PhyAgentOS is a Recursive Self-Improving (RSI) physical agent operating system that enables agents to recursively self-improve through agent |
| [sahibzada-allahyar/Formal-Verification-RSI](https://github.com/sahibzada-allahyar/Formal-Verification-RSI) | self-improvement | 2,882 | `RSI` | Formal verification for AI: a Lean 4 + Dafny proof checker that catches fake AI proofs (reward hacking), and verified recursive self-improve |
| [facebookresearch/HyperAgents](https://github.com/facebookresearch/HyperAgents) | self-improvement | 2,873 | `RSI` | Self-referential self-improving agents that can optimize for any computable task |
| [YeQing17-2026/OmniAgent](https://github.com/YeQing17-2026/OmniAgent) | self-improvement | 2,585 | `RSI` | An agent capable of self-evolving and dynamically hardening security |
| [chrisworsey55/atlas-gic](https://github.com/chrisworsey55/atlas-gic) | autoresearch-system | 2,432 | `AutoResearch` `RSI` | ATLAS by General Intelligence Capital — Self-improving AI trading agents using Karpathy-style autoresearch |
| [guy-hartstein/company-research-agent](https://github.com/guy-hartstein/company-research-agent) | autoresearch-system | 2,314 | `AutoResearch` | An agentic company research tool powered by LangGraph and Tavily that conducts deep diligence on companies using a multi-agent framework. It |
| [AnotiaWang/deep-research-web-ui](https://github.com/AnotiaWang/deep-research-web-ui) | autoresearch-system | 2,225 | `AutoResearch` | AI deep-research agent that turns any question into a cited report: plans searches, reads real sources, verifies evidence. Self-hosted, mult |
| [hyperspaceai/agi](https://github.com/hyperspaceai/agi) | agent-infra | 2,074 | `AutoResearch` | The first distributed AGI system. Thousands of autonomous AI agents collaboratively train models, share experiments via P2P gossip, and push |
| [trevin-creator/autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx) | autoresearch-system | 1,889 | `AutoResearch` | Apple Silicon (MLX) port of Karpathy's autoresearch — autonomous AI research loops on Mac, no PyTorch required. |
| [OS-Copilot/OS-Copilot](https://github.com/OS-Copilot/OS-Copilot) | self-improvement | 1,797 | `RSI` | An self-improving embodied conversational agent seamlessly integrated into the operating system to automate our daily tasks. |
| [mims-harvard/ToolUniverse](https://github.com/mims-harvard/ToolUniverse) | autoresearch-system | 1,777 | `AutoResearch` | Democratizing AI scientists with ToolUniverse |
| [TokenRhythm/NeoHorse](https://github.com/TokenRhythm/NeoHorse) | self-improvement | 1,697 | `RSI` | NeoHorse-1: Towards Recursive Self-Improvement via Agentic Post-Training with Routing Harness. |
| [RightNow-AI/autokernel](https://github.com/RightNow-AI/autokernel) | autoresearch-system | 1,619 | `AutoResearch` | Autoresearch for GPU kernels. Give it any PyTorch model, go to sleep, wake up to optimized Triton kernels. |
| [modelscope/AgentEvolver](https://github.com/modelscope/AgentEvolver) | self-improvement | 1,590 | `RSI` | AgentEvolver: Towards Efficient Self-Evolving Agent System |
| [hexdocom/lemonai](https://github.com/hexdocom/lemonai) | self-improvement | 1,574 | `RSI` | Lemon AI is the first Full-stack Open-source Self-Evolving General AI Agent, offering a fully local alternative to Agentic platforms like Ma |
| [zhengkid/Dream-RSI](https://github.com/zhengkid/Dream-RSI) | self-improvement | 1,573 | `RSI` | The offical repo for "Dream-RSI: Recursive Self-Improvement through Evolving Worlds" |
| [ghostwright/phantom](https://github.com/ghostwright/phantom) | self-improvement | 1,490 | `RSI` | An AI co-worker with its own computer. Self-evolving, persistent memory, MCP server, secure credential collection, email identity. Built on  |
| [InternScience/InternAgent](https://github.com/InternScience/InternAgent) | autoresearch-system | 1,467 | `AutoResearch` | InternAgent-1.5: A Unified Agentic Framework for Long-Horizon Autonomous Scientific Discovery |
| [dzhng/skills](https://github.com/dzhng/skills) | autoresearch-system | 1,454 | `AutoResearch` | Reusable AI agent skills for software factories: explore ideas, write specs, implement, review, and run autonomous research. Works with Clau |
| [CharlesQ9/Self-Evolving-Agents](https://github.com/CharlesQ9/Self-Evolving-Agents) | self-improvement | 1,345 | `RSI` |  |
| [huytieu/COG-second-brain](https://github.com/huytieu/COG-second-brain) | self-improvement | 1,342 | `RSI` | Self-evolving second brain with 35 AI skills, 10 agents, and people CRM. Closed-loop harness: a V-model verification lifecycle where the wor |
| [OpenRaiser/NanoResearch](https://github.com/OpenRaiser/NanoResearch) | other | 1,333 | `AutoResearch` | 🦞+🔬 NanoResearch: The Autonomous AI Research Assistant |
| [greyhaven-ai/autocontext](https://github.com/greyhaven-ai/autocontext) | self-improvement | 1,326 | `AutoResearch` `RSI` | a recursive self-improving harness designed to help your agents (and future iterations of those agents) succeed on any task |
| [aiming-lab/Agent0](https://github.com/aiming-lab/Agent0) | self-improvement | 1,287 | `RSI` | [ICML'26 & COLM'26] Agent0 Series: Self-Evolving Agents from Zero Data |
| [ZHangZHengEric/Sage](https://github.com/ZHangZHengEric/Sage) | agent-infra | 1,211 | `RSI` | An RSI Agent Harness for running, evaluating, and evolving agents—with tools, skills, MCP, stateful execution, and multi-agent workflows. |
| [OpenLAIR/dr-claw](https://github.com/OpenLAIR/dr-claw) | other | 1,200 | `AutoResearch` | A Super AI Lab with massive AI Doctors as Assistants. Best IDE for Research via AI Power. |
| [mattprusak/autoresearch-genealogy](https://github.com/mattprusak/autoresearch-genealogy) | autoresearch-system | 1,191 | `AutoResearch` | Structured prompts, vault templates, and archive guides for AI-assisted genealogy research. Built for Claude Code. |
| [polyuiislab/infiAgent](https://github.com/polyuiislab/infiAgent) | autoresearch-system | 1,189 | `AutoResearch` | Build your own Cowork, AI Scientist and other SoTA Agents just by editing config files. Support anthropic skills. An infinite-horizon agent  |
| [ruc-datalab/EvoOntology](https://github.com/ruc-datalab/EvoOntology) | self-improvement | 1,167 | `RSI` | EvoOntology: A Self-Evolving Ontology Layer for Data Agents ⚙️ EvoOntology插件为Claude Code/Codex 建立&进化本体层 |
| [withkynam/vibecode-pro-max-kit](https://github.com/withkynam/vibecode-pro-max-kit) | self-improvement | 1,167 | `RSI` | Your AI forgets. This remembers. Spec-driven coding harness for vibecoders, product owners, CEOs and real builders — self-improving context  |
| [rashakil-ds/Roadmap-Docs](https://github.com/rashakil-ds/Roadmap-Docs) | other | 1,156 | `AutoResearch` | Best Data Science, Data Analytics, AI, and SDE roadmaps. This repository is continually updated based on the top job postings on LinkedIn an |
| [RUC-NLPIR/Arbor](https://github.com/RUC-NLPIR/Arbor) | autoresearch-system | 1,143 | `AutoResearch` | A generalist autonomous research agent — runs experiments, researches, and iteratively optimizes, autonomously. |
| [Xiangyue-Zhang/auto-deep-researcher-24x7](https://github.com/Xiangyue-Zhang/auto-deep-researcher-24x7) | agent-infra | 1,142 | `AutoResearch` | 🔥 An autonomous AI agent that runs your deep learning experiments 24/7 while you sleep. Zero-cost monitoring, Leader-Worker architecture, co |
| [Gen-Verse/RSI-Anything](https://github.com/Gen-Verse/RSI-Anything) | self-improvement | 1,129 | `RSI` | RSI-Anything: Unlocking Recursive Self-Improvement with World Models |
| [Human-Agent-Society/CORAL](https://github.com/Human-Agent-Society/CORAL) | autoresearch-system | 1,123 | `AutoResearch` `RSI` | Open-source autoresearch powered by autonomous coding agents. Run Claude Code, OpenCode, and Codex with grading, shared knowledge, and multi |
| [opencrabs/opencrabs](https://github.com/opencrabs/opencrabs) | deep-research | 1,026 | `RSI` | The all-in-one AI agent. Build mobile apps, frontend, backend, manages files, deep research, schedule tasks and events. Self-improving, self |
| [wangziqi06/724-office](https://github.com/wangziqi06/724-office) | self-improvement | 1,020 | `RSI` | 7/24 Office — Self-evolving AI Agent system. 36 tools, 10,000 lines pure Python, modular architecture, MCP plugins, three-layer memory, nudg |
| [xvirobotics/metabot](https://github.com/xvirobotics/metabot) | self-improvement | 1,005 | `RSI` | 构建受监督的、自我进化的 Agent 组织的基础设施 \| Infrastructure for supervised, self-improving agent organization. 飞书/Telegram 手机端运行 Claude Code 或 Kimi Code（双引 |
| [olelehmann1337/autoresearch-skill](https://github.com/olelehmann1337/autoresearch-skill) | autoresearch-system | 980 | `AutoResearch` |  |
| [mikekelly/AgentK](https://github.com/mikekelly/AgentK) | self-improvement | 969 | `RSI` | An autoagentic AGI that is self-evolving and modular. |
| [Kulaxyz/self-learning-skills](https://github.com/Kulaxyz/self-learning-skills) | self-improvement | 968 | `RSI` | A self-improving skill for AI coding agents (Claude Code, Cursor, AGENTS.md): recognize a hard-won golden path in a session and harvest it i |
| [zamalali/DeepGit](https://github.com/zamalali/DeepGit) | autoresearch-system | 927 | `AutoResearch` | Deep research agent to help you find the best GitHub repositories 🕵️! |
| [openmemind/memind](https://github.com/openmemind/memind) | self-improvement | 906 | `RSI` | Self-evolving cognitive memory and context engine for AI agents in Java. Empowering 24/7 proactive agents like OpenClaw with understanding a |

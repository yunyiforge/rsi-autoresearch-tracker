# RSI & AutoResearch Benchmark 数据集

> 自动生成于 2026-11-11T07:45:23Z（UTC）。精选 16 个 + 自动发现候选 67 个；论文复现任务候选 111 个。构建方法见 [docs/BENCHMARK_PIPELINE.md](../docs/BENCHMARK_PIPELINE.md)。

## 精选 Benchmark

| Benchmark | 方向 | 机构 | 年份 | 规模 | 指标 | 论文 | ⭐ |
|---|---|---|---|---|---|---|---:|
| [METR Time Horizon](https://arxiv.org/abs/2503.14499) | ai-rnd | METR | 2025 |  | 50% 成功率对应的人类任务时长（time horizon） | [arXiv](https://arxiv.org/abs/2503.14499) |  |
| [MLRC-Bench](https://arxiv.org/abs/2504.09702) | ai-rnd |  | 2025 |  | 相对基线与人类最佳方案的提升 | [arXiv](https://arxiv.org/abs/2504.09702) |  |
| [RE-Bench](https://arxiv.org/abs/2411.15114) | ai-rnd | METR | 2024 | 7 个开放式 ML 研究工程环境 | 相对参考解的归一化得分，并与人类专家 8 小时成绩对比 | [arXiv](https://arxiv.org/abs/2411.15114) |  |
| [SWE-bench](https://github.com/SWE-bench/SWE-bench) | coding | Princeton | 2023 | 2,294 个 GitHub issue（Verified 子集 500） | 解决率 (% Resolved) | [arXiv](https://arxiv.org/abs/2310.06770) | 6,170 |
| [HCAST](https://arxiv.org/abs/2503.17354) | general-agent | METR | 2025 | 189 个软件/ML/网络安全任务 | 按人类完成时长校准的成功率 | [arXiv](https://arxiv.org/abs/2503.17354) |  |
| [MLAgentBench](https://github.com/snap-stanford/MLAgentBench) | ml-engineering | Stanford | 2023 | 13 个 ML 实验任务 | 相对基线提升 ≥10% 的成功率 | [arXiv](https://arxiv.org/abs/2310.03302) | 360 |
| [MLE-bench](https://github.com/openai/mle-bench) | ml-engineering | OpenAI | 2024 | 75 个 Kaggle 竞赛 | 获得 Kaggle 奖牌的比例 | [arXiv](https://arxiv.org/abs/2410.07095) | 1,794 |
| [MLGym](https://github.com/facebookresearch/MLGym) | ml-engineering | Meta | 2025 | 13 个跨领域 AI 研究任务 | performance profile / AUP | [arXiv](https://arxiv.org/abs/2502.14499) | 625 |
| [CORE-Bench](https://github.com/siegelz/core-bench) | paper-replication | Princeton | 2024 | 来自 90 篇论文的 270 个任务 | 准确率 | [arXiv](https://arxiv.org/abs/2409.11363) | 80 |
| [PaperBench](https://github.com/openai/preparedness) | paper-replication | OpenAI | 2025 | 20 篇 ICML 2024 论文，约 8,316 个可打分子任务 | 基于层级 rubric 的复现得分（LLM judge 评分） | [arXiv](https://arxiv.org/abs/2504.01848) | 1,340 |
| [SUPER](https://github.com/allenai/super-benchmark) | paper-replication | AI2 | 2024 | 45 个专家问题 + 152 个子问题 + 604 个自动生成问题 | 任务成功率 | [arXiv](https://arxiv.org/abs/2409.07440) | 58 |
| [BixBench](https://github.com/Future-House/BixBench) | scientific-discovery | FutureHouse | 2025 |  | 开放式答案准确率 | [arXiv](https://arxiv.org/abs/2503.00096) | 153 |
| [DiscoveryWorld](https://github.com/allenai/discoveryworld) | scientific-discovery | AI2 | 2024 | 120 个虚拟科学发现任务 | 任务完成度 / 解释性知识得分 | [arXiv](https://arxiv.org/abs/2406.06769) | 229 |
| [LAB-Bench](https://github.com/Future-House/LAB-Bench) | scientific-discovery | FutureHouse | 2024 | 2,400+ 道生物学研究实务题 | 准确率 / 精确率 | [arXiv](https://arxiv.org/abs/2407.10362) | 136 |
| [SciCode](https://github.com/scicode-bench/SciCode) | scientific-discovery |  | 2024 | 80 个主问题 / 338 个子问题 | 通过率 | [arXiv](https://arxiv.org/abs/2407.13168) | 246 |
| [ScienceAgentBench](https://github.com/OSU-NLP-Group/ScienceAgentBench) | scientific-discovery | OSU NLP | 2024 | 来自 44 篇论文的 102 个任务 | 成功率 / CodeBERTScore | [arXiv](https://arxiv.org/abs/2410.05080) | 184 |

## 自动发现的 Benchmark 候选

按方向统计：general-agent 19，coding 15，research-ideation 12，self-improvement 8，scientific-discovery 5，ai-rnd 4，ml-engineering 2，paper-replication 2

| 名称 | 方向 | 年份 | 论文 | 仓库 | 首次发现 |
|---|---|---|---|---|---|
| Toward Autonomous RTL and Synthesis Optimization: Benchmarking and Self-Improvi… | self-improvement | 2026 | [arXiv](https://arxiv.org/abs/2611.13713) |  | 2026-11-11 |
| ARE-bench | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2611.14364) |  | 2026-11-11 |
| DeepResearch RewardBench | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2611.10156) |  | 2026-11-10 |
| Causal Discovery Bench | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2611.09934) | [mshen1019/causal-discovery-bench](https://github.com/mshen1019/causal-discovery-bench) | 2026-11-10 |
| What Are LLM Agents Actually Learning on Low-Budget Molecular Optimization Benc… | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2611.08522) |  | 2026-11-09 |
| Flex-RSI | self-improvement | 2026 | [arXiv](https://arxiv.org/abs/2611.08946) |  | 2026-11-09 |
| CompressionBench | coding | 2026 | [arXiv](https://arxiv.org/abs/2611.06858) |  | 2026-11-05 |
| When Agent Evaluation Becomes Unreliable | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2610.16067) |  | 2026-11-03 |
| VibeTraining-Bench | coding | 2026 | [arXiv](https://arxiv.org/abs/2610.26342) | [D2I-ai/VibeTraining-Bench](https://github.com/D2I-ai/VibeTraining-Bench) | 2026-11-03 |
| TSFLab | coding | 2026 | [arXiv](https://arxiv.org/abs/2610.40901) | [D2I-Group/TSFLab](https://github.com/D2I-Group/TSFLab) | 2026-11-03 |
| TruthInsightBench | research-ideation | 2026 | [arXiv](https://arxiv.org/abs/2609.05079) | [TruthInsight-stack/TruthInsightBench](https://github.com/TruthInsight-stack/TruthInsightBench) | 2026-11-03 |
| Trace Evolution Bench | coding | 2026 | [arXiv](https://arxiv.org/abs/2610.15055) |  | 2026-11-03 |
| Testing-Driven Reliability Audit of Trajectory-Based Early Outcome Prediction f… | coding | 2026 | [arXiv](https://arxiv.org/abs/2609.25647) |  | 2026-11-03 |
| SWE-bench-Style | coding | 2026 | [arXiv](https://arxiv.org/abs/2610.39417) |  | 2026-11-03 |
| StableEval Arena | coding | 2026 | [arXiv](https://arxiv.org/abs/2609.18949) |  | 2026-11-03 |
| SoundnessBench | ai-rnd | 2026 | [arXiv](https://arxiv.org/abs/2605.30329) |  | 2026-11-03 |
| SelfImprove-Bench | self-improvement | 2026 | [arXiv](https://arxiv.org/abs/2611.02797) |  | 2026-11-03 |
| SEABench | self-improvement | 2026 | [arXiv](https://arxiv.org/abs/2609.35596) |  | 2026-11-03 |
| Sci$Π$vot | scientific-discovery | 2026 | [arXiv](https://arxiv.org/abs/2610.21082) |  | 2026-11-03 |
| Sci-MMR | research-ideation | 2026 | [arXiv](https://arxiv.org/abs/2609.11243) |  | 2026-11-03 |
| RSI Arena | self-improvement | 2026 | [arXiv](https://arxiv.org/abs/2610.33624) |  | 2026-11-03 |
| RobotAgentBench | self-improvement | 2026 | [arXiv](https://arxiv.org/abs/2610.34649) |  | 2026-11-03 |
| ResearchClawBench | general-agent | 2026 |  | [InternScience/ResearchClawBench](https://github.com/InternScience/ResearchClawBench) | 2026-11-03 |
| RATIO | research-ideation | 2026 | [arXiv](https://arxiv.org/abs/2608.27394) |  | 2026-11-03 |
| ProteinGeoBench | scientific-discovery | 2026 | [arXiv](https://arxiv.org/abs/2610.26829) | [Protege-AI/ProteinGeoBench](https://github.com/Protege-AI/ProteinGeoBench) | 2026-11-03 |
| ProjectionBench | research-ideation | 2026 | [arXiv](https://arxiv.org/abs/2605.30284) |  | 2026-11-03 |
| PostTrainBench | ai-rnd | 2026 | [arXiv](https://arxiv.org/abs/2603.08640) |  | 2026-11-03 |
| ParetoRSI-Gym | ml-engineering | 2026 | [arXiv](https://arxiv.org/abs/2610.34386) |  | 2026-11-03 |
| PAPERBENCHX | paper-replication | 2026 | [arXiv](https://arxiv.org/abs/2610.39744) |  | 2026-11-03 |
| Novel or Not? PatEx-Gym | research-ideation | 2026 | [arXiv](https://arxiv.org/abs/2610.33503) |  | 2026-11-03 |
| More Rules, Longer Lists? Benchmarking Self-Evolving Agents on a Hidden-Rule Cu… | self-improvement | 2026 | [arXiv](https://arxiv.org/abs/2610.40758) |  | 2026-11-03 |
| MMPostTrainBench | research-ideation | 2026 | [arXiv](https://arxiv.org/abs/2610.05398) | [sod1010/MMPostTrainBench](https://github.com/sod1010/MMPostTrainBench) | 2026-11-03 |
| MedHopQA | research-ideation | 2026 | [arXiv](https://arxiv.org/abs/2605.12361) |  | 2026-11-03 |
| M4Bench | coding | 2026 | [arXiv](https://arxiv.org/abs/2610.37459) | [hannesill/m4](https://github.com/hannesill/m4) | 2026-11-03 |
| LifeSearch | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2610.18092) |  | 2026-11-03 |
| Identical Runs, Different Results | coding | 2026 | [arXiv](https://arxiv.org/abs/2609.33812) | [earino/identical-runs-different-results](https://github.com/earino/identical-runs-different-results) | 2026-11-03 |
| GameReplica | coding | 2026 | [arXiv](https://arxiv.org/abs/2609.22308) |  | 2026-11-03 |
| From Scientific Observations to Mechanisms: Benchmarking Hypothesis Generation… | research-ideation | 2026 | [arXiv](https://arxiv.org/abs/2610.05197) |  | 2026-11-03 |
| From Evaluation to Evolution | self-improvement | 2026 | [arXiv](https://arxiv.org/abs/2610.41210) |  | 2026-11-03 |
| FALSIFYBENCH | research-ideation | 2026 | [arXiv](https://arxiv.org/abs/2606.04751) |  | 2026-11-03 |
| EvoCowork | coding | 2026 | [arXiv](https://arxiv.org/abs/2610.14828) | [DeepThinkingZhouLiu/cowork-evolution-benchmark](https://github.com/DeepThinkingZhouLiu/cowork-evolution-benchmark) | 2026-11-03 |
| EmbodiedCLBench | coding | 2026 | [arXiv](https://arxiv.org/abs/2610.13021) |  | 2026-11-03 |
| DrugTargetWorld | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2610.09558) | [sammargolis/DrugTargetWorld](https://github.com/sammargolis/DrugTargetWorld) | 2026-11-03 |
| DataSense-Bench | coding | 2026 | [arXiv](https://arxiv.org/abs/2610.12190) | [DataSense-Bench/DataSense-Bench](https://github.com/DataSense-Bench/DataSense-Bench) | 2026-11-03 |
| CentaurBench | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2608.18554) |  | 2026-11-03 |
| Can Coding Agents Reproduce Official Statistics? Metadata, Retry Budget and the… | coding | 2026 | [arXiv](https://arxiv.org/abs/2609.22222) |  | 2026-11-03 |
| Beyond Watching and Searching | coding | 2026 | [arXiv](https://arxiv.org/abs/2610.31158) | [marinero4972/OmniDR-Bench](https://github.com/marinero4972/OmniDR-Bench) | 2026-11-03 |
| Benchmarking Automated Security Patch Backporting: How Far Are We? | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2608.17671) |  | 2026-11-03 |
| Benchmarking Argumentative Behaviour of LLMs: A Study of Defences Against Chara… | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2609.28673) |  | 2026-11-03 |
| Benchmarking and Error Analysis of Deep Search and Deep Research LLM Agents | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2610.29346) |  | 2026-11-03 |
| awesome-ai-auto-research | general-agent | 2026 |  | [worldbench/awesome-ai-auto-research](https://github.com/worldbench/awesome-ai-auto-research) | 2026-11-03 |
| Auto-Research Arena | research-ideation | 2026 | [arXiv](https://arxiv.org/abs/2610.35866) | [Auto-Research-Arena/auto-research-arena](https://github.com/Auto-Research-Arena/auto-research-arena) | 2026-11-03 |
| Auto-MD-bench | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2610.25069) | [Edwin0080/Auto-MD-bench](https://github.com/Edwin0080/Auto-MD-bench) | 2026-11-03 |
| ARAC | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2608.12788) |  | 2026-11-03 |
| AgentIdeaBench | research-ideation | 2026 | [arXiv](https://arxiv.org/abs/2609.07611) | [HKUST-KnowComp/AgentIdeaBench](https://github.com/HKUST-KnowComp/AgentIdeaBench) | 2026-11-03 |
| Agentic Commerce Bench | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2609.35886) | [BuildWithGordonAI/agentcommercebench](https://github.com/BuildWithGordonAI/agentcommercebench) | 2026-11-03 |
| AFDBench | general-agent | 2026 | [arXiv](https://arxiv.org/abs/2608.24954) |  | 2026-11-03 |
| Adversarial Fast-Moving Real-World Domains as Test Beds for Benchmarking AI Sci… | paper-replication | 2026 | [arXiv](https://arxiv.org/abs/2608.03569) |  | 2026-11-03 |
| When AI Co-Scientists Fail | research-ideation | 2025 | [arXiv](https://arxiv.org/abs/2505.11855) |  | 2026-11-03 |
| TimeSeriesGym | ml-engineering | 2025 | [arXiv](https://arxiv.org/abs/2505.13291) | [moment-timeseries-foundation-model/TimeSeriesGym](https://github.com/moment-timeseries-foundation-model/TimeSeriesGym) | 2026-11-03 |
| SGI-Bench | scientific-discovery | 2025 |  | [InternScience/SGI-Bench](https://github.com/InternScience/SGI-Bench) | 2026-11-03 |
| PhysGym | scientific-discovery | 2025 |  | [principia-ai/PhysGym](https://github.com/principia-ai/PhysGym) | 2026-11-03 |
| HeurekaBench | scientific-discovery | 2025 |  | [mlbio-epfl/HeurekaBench](https://github.com/mlbio-epfl/HeurekaBench) | 2026-11-03 |
| EXP-Bench | ai-rnd | 2025 | [arXiv](https://arxiv.org/abs/2505.24785) | [Just-Curieous/Curie](https://github.com/Just-Curieous/Curie) | 2026-11-03 |
| deep_research_bench | general-agent | 2025 |  | [Ayanami0730/deep_research_bench](https://github.com/Ayanami0730/deep_research_bench) | 2026-11-03 |
| BaisBench | general-agent | 2025 |  | [EperLuo/BaisBench](https://github.com/EperLuo/BaisBench) | 2026-11-03 |
| ablation-bench | ai-rnd | 2025 |  | [ai-scientist-bench/ablation-bench](https://github.com/ai-scientist-bench/ablation-bench) | 2026-11-03 |

## 论文复现任务候选（自动构建）

共 111 个（难度提示：easy 4，hard 17，medium 90）。完整数据见 [`data/benchmark_tasks.jsonl`](../data/benchmark_tasks.jsonl)。

| 任务 | 论文 | 官方代码 | 难度 |
|---|---|---|---|
| `replicate:2611.12000` | [HyPLM Technical Report](https://arxiv.org/abs/2611.12000) | [Tencent-Hunyuan/hyra-results](https://github.com/Tencent-Hunyuan/hyra-results) | hard |
| `replicate:2611.11997` | [HyInv Technical Report](https://arxiv.org/abs/2611.11997) | [Tencent-Hunyuan/Hyra-results](https://github.com/Tencent-Hunyuan/Hyra-results) | hard |
| `replicate:2611.13006` | [Seeing Is Not Believing: Counterfactual Lesion Erasure Teaches a Small Medical Vision-Language Agent to Report Only What the Image Shows](https://arxiv.org/abs/2611.13006) | [bhaskargurram-ai/medscope](https://github.com/bhaskargurram-ai/medscope) | easy |
| `replicate:2611.11558` | [InfraRSI: Harnessing Recursive Self-Improvement for Training Infrastructure](https://arxiv.org/abs/2611.11558) | [TokenRhythm/InfraRSI](https://github.com/TokenRhythm/InfraRSI) | hard |
| `replicate:2611.11212` | [Deterministic Narrative Gravity: Bridging Theory of Mind and Historical Simulation through ABM-LLM Architectures](https://arxiv.org/abs/2611.11212) | [alixiacf/cognitive-abm](https://github.com/alixiacf/cognitive-abm) | medium |
| `replicate:2611.10748` | [REINS: A Self-Evolving Agent Harness for Real-Time Trajectory Planning](https://arxiv.org/abs/2611.10748) | [ZhihongCui/REINS](https://github.com/ZhihongCui/REINS) | medium |
| `replicate:2611.10719` | [No Second Run: Does RSI Stop at Frontier Pre-training?](https://arxiv.org/abs/2611.10719) | [GAIR-NLP/801-30B](https://github.com/GAIR-NLP/801-30B) | hard |
| `replicate:2611.08922` | [Glyph: An Interpretability Engine for AI-Driven Scientific Discovery in Clinical Data](https://arxiv.org/abs/2611.08922) | [StanfordMIMI/Glyph](https://github.com/StanfordMIMI/Glyph) | medium |
| `replicate:2611.01918` | [AgenticMobility: An Open-Source Platform for Multi-AI-Agent Mobility Dynamics](https://arxiv.org/abs/2611.01918) | [Agentic-City-Research/Agentic-Mobility](https://github.com/Agentic-City-Research/Agentic-Mobility) | medium |
| `replicate:2611.01840` | [Self-Evolving Agentic Workflows via Semantic Decomposition of Complex Tasks](https://arxiv.org/abs/2611.01840) | [Applied-Machine-Learning-Lab/NeurIPS2026_SeaFlow](https://github.com/Applied-Machine-Learning-Lab/NeurIPS2026_SeaFlow) | medium |
| `replicate:2611.03721` | [Counterexample-driven autonomous research with application to excess radiated energy in a Z-pinch](https://arxiv.org/abs/2611.03721) | [tomzhu0225/simjecture](https://github.com/tomzhu0225/simjecture) | medium |
| `replicate:2610.40589` | [Collaborative AI agents for autonomous experimental research with solid-state quantum spins](https://arxiv.org/abs/2610.40589) | [E-zClap/auctopus](https://github.com/E-zClap/auctopus) | medium |
| `replicate:2610.40488` | [rTaste: Do Research Agents Have Taste? Evaluating Early Stage Research Judgment](https://arxiv.org/abs/2610.40488) | [ArtKanke/rTaste](https://github.com/ArtKanke/rTaste) | medium |
| `replicate:2610.38691` | [Beyond fabrication: Misattributed numbers in papers written by AI research agents](https://arxiv.org/abs/2610.38691) | [mos3b-faqeeh/agent-integrity-analysis](https://github.com/mos3b-faqeeh/agent-integrity-analysis) | medium |
| `replicate:2610.37741` | [Agentic Backdoors via Pretraining Poisoning](https://arxiv.org/abs/2610.37741) | [safety-research/agentic-backdoor](https://github.com/safety-research/agentic-backdoor) | hard |
| `replicate:2610.37459` | [M4Bench: Evaluating Procedural Specification for Clinical EHR Derivation Agents](https://arxiv.org/abs/2610.37459) | [hannesill/m4](https://github.com/hannesill/m4) | medium |
| `replicate:2610.36511` | [Do AI Scientists Know What's New?](https://arxiv.org/abs/2610.36511) | [emmatliu/claimnov](https://github.com/emmatliu/claimnov) | medium |
| `replicate:2610.40685` | [Agentic Systems for Calibrating Cosmological Simulations](https://arxiv.org/abs/2610.40685) | [chaipattira/SimulationCalibrator](https://github.com/chaipattira/SimulationCalibrator) | medium |
| `replicate:2610.35866` | [Auto-Research Arena: Benchmarking and Advancing Auto-Research in Language Modeling](https://arxiv.org/abs/2610.35866) | [Auto-Research-Arena/auto-research-arena](https://github.com/Auto-Research-Arena/auto-research-arena) | hard |
| `replicate:2610.35793` | [Quantifying Claim Smoothing by LLM Research Agents](https://arxiv.org/abs/2610.35793) | [tiasa2/SmoothScore](https://github.com/tiasa2/SmoothScore) | medium |
| `replicate:2610.33845` | [Build, Don't Play: Self-Improving LLM Research Agents Develop a Hearthstone Battlegrounds AI That Rivals Top Players](https://arxiv.org/abs/2610.33845) | [MCG-NJU/AutoTavern](https://github.com/MCG-NJU/AutoTavern) | medium |
| `replicate:2610.33465` | [LegoSR: A Unified Framework for Self-improving Agent-Guided Scientific Discovery](https://arxiv.org/abs/2610.33465) | [Scientific-Artificial-Intelligence-Lab/kd](https://github.com/Scientific-Artificial-Intelligence-Lab/kd) | medium |
| `replicate:2610.32813` | [HarnessMM: Recursive Self-Improvement for Harness Token Efficiency](https://arxiv.org/abs/2610.32813) | [YuhuaJiang2002/HarnessMM](https://github.com/YuhuaJiang2002/HarnessMM) | medium |
| `replicate:2610.31158` | [Beyond Watching and Searching: Benchmarking Agents for Video-centered Deep Research Reports](https://arxiv.org/abs/2610.31158) | [marinero4972/OmniDR-Bench](https://github.com/marinero4972/OmniDR-Bench) | medium |
| `replicate:2610.28577` | [Cache Engineering for Agents](https://arxiv.org/abs/2610.28577) | [thu-nics/AKV](https://github.com/thu-nics/AKV) | medium |
| `replicate:2610.26829` | [ProteinGeoBench: Frontier Structural-Biology Agents Are Fluent at Lookup but Lost in Geometry](https://arxiv.org/abs/2610.26829) | [Protege-AI/ProteinGeoBench](https://github.com/Protege-AI/ProteinGeoBench) | medium |
| `replicate:2610.26770` | [HarnessPro: Recursive Harness Self-Improvement with Pareto Optimization for Performance-Cost Trade-offs](https://arxiv.org/abs/2610.26770) | [pzs19/HarnessPro](https://github.com/pzs19/HarnessPro) | medium |
| `replicate:2610.26632` | [When the harness decides success: state that cannot be re-observed](https://arxiv.org/abs/2610.26632) | [raimondasl/persistgym](https://github.com/raimondasl/persistgym) | medium |
| `replicate:2610.26469` | [VeriCUA: Learning Proactive Verification for Reliable GUI Agent Rewards](https://arxiv.org/abs/2610.26469) | [Jeffjeno/VeriCUA](https://github.com/Jeffjeno/VeriCUA) | hard |
| `replicate:2610.26453` | [Learning What to Remember: Resource-Efficient Self-Improvement for Lifelong Agents](https://arxiv.org/abs/2610.26453) | [AIGNLAI/TokenWorth](https://github.com/AIGNLAI/TokenWorth) | medium |

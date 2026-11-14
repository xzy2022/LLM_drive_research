# Highway-env × 大模型：2023–2026 年研究版图核查

## 结论先行

截至 **2026 年 11 月 7 日**，我能核实到的 Highway-env / 基于 Highway-env 构建的基准中“大模型承担实质角色”的研究，已经从 2023–2024 年的“LLM 直接逐步做高层驾驶决策”扩展为几条相当清晰的支线：**闭环决策与记忆、LLM→RL 先验/安全约束、显式安全过滤、奖励生成、程序/规则生成、多车协同，以及自然语言指令执行**。其中最拥挤的已经不是单纯“让 GPT 开车”，而是 **(a) 逐步决策、(e) 给 RL/规划器提供先验、(f) 安全过滤/验证和 (h) 记忆、反思、世界知识等辅助角色**；相比之下，**可系统评测的人类自然语言指令、一次性策略程序生成、奖励设计和多智能体协同仍明显更稀疏**。citeturn916061search1turn582189search0turn132438search0

用户给出的清单中有几处值得修正：**LA-RL 明确使用 Highway-env 的 `highway-v0`，并非“实验平台待核实”**；KoMA 的 IEEE TIV 卷期在 2025 年，但 IEEE 记录的首次在线发表日期是 **2024 年 11 月 6 日**；SanDRA 截至检索日已经是 IEEE T-ITS Early Access 正式发表，而不是“仅接收”；GAPL、LA-RL 等仍是预印本。citeturn306303view1turn882491search1turn307398search2turn632919academia7

指令执行方面，真正形成专门 benchmark 的核心仍然是 **LaMPilot-Bench**；`Receive, Reason, and React` 则提供了一个非常重要但规模小得多的反例：它明确测试了“用户要求超车，但场景并不安全”的情况，因此目前我能核实到的 Highway-env 文献中，**“与安全冲突的自然语言命令”并非完全空白**。但是，**歧义指令、同义改写一致性、需要澄清的指令、暂时不可执行指令的专门等待/拒绝评分、复杂多条件持续约束**，我均未找到专门且成体系的 Highway-env 评测。citeturn916061search6turn352544search0turn352544search7

另一个重要结论是：论文越来越明确承认 Highway-env 的“抽象状态 + 简化交通模型”问题。LORD 直接指出其车辆渲染只是矩形、落在视觉大模型训练分布之外；SEDM 则明确把“结构化道路、正常交通动力学、完美状态输入、不经过原始感知”列为外部有效性限制。citeturn565815view0turn116598view0

## 工作总表与角色分类

下表只纳入我能找到 **Highway-env/其派生环境的直接实验依据** 的工作。对于模型、训练量或仓库内容没有可靠的一手证据时，我宁可写“未核实/未看到”。“实见”是指本次检索确实看到公开仓库文件树或 README，而不是论文仅声称“代码已发布”。

| 工作 | 发表状态 | 大模型角色 | 人类自然语言指令/偏好 | 训练 | 大模型 | 评测平台与主要指标 | 代码：声称 / 实见 |
|---|---|---|---|---|---|---|---|
| **Drive Like a Human: Rethinking Autonomous Driving with Large Language Models** — Daocheng Fu, 2024 | 已发表，WACV Workshops 2024；DOI 10.1109/WACVW60836.2024.00102 | a, h：逐步决策、语言推理 | 否，主要是场景文本 | LLM 不训练；闭环直接推理 | GPT 系列；公开实现使用 OpenAI 接口 | Highway-env；安全、效率、闭环行为 | 声称公开 / **实见 GitHub 仓库** citeturn606724search0turn712321search1 |
| **Receive, Reason, and React: Drive as You Say with Large Language Models in Autonomous Vehicles** — Can Cui, 2024 | 已发表，IEEE ITS Magazine 16(4)；DOI 10.1109/MITS.2024.3381793 | a, c：命令理解与在线决策 | **是**：超车、激进/保守风格；含不安全超车请求 | 无 LLM 微调证据 | GPT-4 | HighwayEnv；Table I 报加速度、转角、速度、间距、时间、换道等 | 论文项目页可见；完整实现树本次未确认 citeturn352544search0turn352544search2turn352544search7 |
| **DiLu: A Knowledge-Driven Approach to Autonomous Driving with Large Language Models** — Licheng Wen, 2024 | **已发表，ICLR 2024**；arXiv:2309.16292 | a, h；并具有 c 的接口能力 | **支持**用户输入 driving intention；正式实验默认安全意图 | 不训练基础 LLM；经验记忆在线积累 | GPT 系列 | Highway-env 闭环；不同车道/交通密度、泛化、memory/reflection | 声称公开 / **实见完整仓库** citeturn916061search0turn916061search1turn916061search7 |
| **LaMPilot: An Open Benchmark Dataset for Autonomous Driving with Language Model Programs** — Yunsheng Ma, 2024 | **已发表，CVPR 2024**；arXiv:2312.04372；DOI 10.1109/CVPR52733.2024.01434 | **b, c**：自然语言→可执行驾驶程序 | **是** | 不微调；0-shot、3-shot、RAG/human feedback | Llama 2-70B-chat、PaLM 2 code-bison、GPT-3.5-turbo、GPT-4、GPT-4 Turbo | **LaMPilot-Bench / HighwayEnv**；completion、collision、TTC、SV、TE、Driving Score | 声称公开 / **实见代码、env、evaluators、prompts** citeturn916061search6turn916061search3turn916061search5 |
| **Human-centric Reward Optimization for Reinforcement Learning-based Automated Driving using Large Language Models** — Ziqi Zhou, 2024 | **仅预印本**；arXiv:2405.04135 | d, e：自然语言偏好→RL reward | **是，但作用在奖励设计而非在线驾驶指令** | DQN 训练；LLM 零样本/提示，不微调 | **GPT-3.5-turbo-1106** | customized HighwayEnv；human-like behavior、reward shaping | arXiv 声称实验数据和源码可用；文件树本次未看到 citeturn582189academia6turn116598view4 |
| **Generating and Evolving Reward Functions for Highway Driving with Large Language Models** — Xu Han, 2024 | **已发表，ITSC 2024**；arXiv:2406.10540；DOI 10.1109/ITSC58415.2024.10919977 | d, e：LLM 生成并演化 reward code | 否 | RL policy 训练；LLM 负责 reward 生成/反思 | 可访问材料中具体型号未充分核实 | Highway-env，多交通配置；success/reward | 代码状态本次未看到可验证文件树 citeturn224955academia2turn148788search4 |
| **LORD: Large Models Based Opposite Reward Design for Autonomous Driving** — Xin Ye, 2025 | **已发表，WACV 2025**；arXiv:2403.18965；DOI 10.1109/WACV61041.2025.00496 | d, e：大预训练模型作为 zero-shot reward | 否 | PPO 等策略训练；预训练大模型不微调 | CLIP、S3D 等视觉/视频/语言预训练模型 | Highway-env；reward quality、驾驶安全/效率 | 本次未看到可核实完整代码树 citeturn512782search4turn512782search5turn512782search8 |
| **Hybrid-Driving: An Autonomous Driving Decision Framework Integrating Large Language Models, Knowledge Graphs and Driving Rules** — Jiabao Wang, 2025 | **已发表，AAAI 2025**；DOI 10.1609/aaai.v39i1.32066 | a, f, h：LLM+知识图谱+规则过滤 | 否 | LLM 本身不训练 | ChatGPT-3.5 | Highway-env 三类场景；success/collision 等；**Fig. 7** 给出对照 | 本次未确认完整公开仓库 citeturn224955search1 |
| **KoMA: Knowledge-Driven Multi-Agent Framework for Autonomous Driving With Large Language Models** — Kemou Jiang, 2024/2025 | **已发表**；IEEE TIV，在线 2024-11-06、卷期 2025；DOI 10.1109/TIV.2024.3488793 | a, g, h：多智能体协同、知识/记忆 | 否 | 无基础 LLM 微调；memory/RAG | 主实验 GPT-4；并比较 GPT-3.5、Llama 2/3、Qwen2 等 | Highway-env on-ramp merging；安全/效率/协作 | 项目页声称代码；**本次看到公开项目/仓库入口** citeturn882491search1turn882491search0turn676860search6turn676860search7 |
| **Towards Interactive and Learnable Cooperative Driving Automation: a Large Language Model-Driven Decision-Making Framework** — Shiyu Fang, 2025 | **已发表，IEEE TVT 2025**；arXiv:2409.12812；DOI 10.1109/TVT.2025.3552922 | a, g, h：协同谈判、分布式决策、记忆 | 否 | LLM 不需专门训练 | GPT 系 LLM | 定制 Highway-env intersection/merge/highway | 声称公开 / **实见 GitHub 代码树** citeturn676860search2turn224955academia0turn676860search3 |
| **AgentsCoDriver: Large Language Model Empowered Collaborative Driving with Lifelong Learning** — Senkang Hu, 2024 | **仅预印本**；arXiv:2404.06345 | a, g, h：协作通信、memory/reflection/lifelong learning | 否 | 不以基础模型微调为核心 | GPT 系 LLM | HighwayEnv 多车协同 | 公开实现状态本次未充分核实 citeturn854011academia9turn854011search4 |
| **Enhancing Autonomous Vehicle Training with Language Model Integration and Critical Scenario Generation (CRITICAL)** — Hanlin Tian, 2024 | **仅预印本**；arXiv:2404.08570 | e, h：LLM 分析/生成 critical scenarios 辅助 RL | 否 | PPO 等 RL 训练 | LLM 可选模块；具体型号未充分核实 | HighwayEnv | 声称公开 / **实见 GitHub 仓库** citeturn606724search6turn606724search3 |
| **PADriver: Towards Personalized Autonomous Driving** — Genghua Kou, 2025 | **已发表，IJCNN 2025**；arXiv:2505.05240；DOI 10.1109/IJCNN64981.2025.11228638 | a, c：MLLM 个性化驾驶 | **是：慢/正常/快等 personalized prompt** | **需要训练/适配**；PAD-Highway 共约 250 h | 可访问版本报告 Vicuna/CLIP 系 MLLM | **PAD-Highway（Highway-env 派生）**；个性化、安全、效率 | 未核实到官方完整代码树 citeturn307398search0turn307398academia3turn676860search5 |
| **Large language model guided deep reinforcement learning for safe autonomous vehicle decision making** — 第一作者见正式论文记录，2026 | **已发表，Transportation Research Part C**；DOI 10.1016/j.trc.2025.105511；预印本题名 *Large Language Model guided Deep Reinforcement Learning for Decision Making in Autonomous Driving*, arXiv:2412.18511 | e, f：LLM expert 约束/干预 DRL | 否 | **DRL 训练** | 可访问摘要未足以可靠确定型号 | Highway-env | 项目页声称 code；本次未见可确认实现树 citeturn604291search0turn604291academia8turn604291search1 |
| **ADRD: LLM-Driven Autonomous Driving Based on Rule-based Decision Systems** — Fanzhi Zeng, 2025 | **仅预印本**；arXiv:2506.14299 | **b, f**：LLM 生成、测试、修正规则式 executable policy | 否 | 无在线 LLM 训练；规则迭代 | 未核实 | Highway-env 三类场景的证据来自论文相关索引/后续比较 | 代码未看到 citeturn521830academia9turn521830search3 |
| **BladeRunner-AD: Adversarial Co-evolution of Robust and Interpretable Driving Policies via LLM Agent Games** — 2025 | **已发表，IEEE MESA 2025**；DOI 10.1109/MESA68091.2025.11278881 | **b, f, h**：Policy Defender 生成决策树，Attacker 造对抗场景 | 否 | 策略通过 agent-game 迭代，不是 RL 微调 | 两个 LLM agents，具体 backbone 未从 IEEE 摘要核实 | **Highway-env**；独立 adversarial test set、collision robustness | 代码未看到 citeturn582189search0 |
| **RESPOND: Risk-Enhanced Structured Pattern for LLM-driven Online Node-level Decision-making in Autonomous Driving** — Dan Chen, 2026 | **已发表，Communications in Transportation Research 2026**；arXiv:2512.20179；DOI 10.26599/COMMTR.2026.9640037 | a, c, h：风险结构化、memory、human feedback/style adaptation | **是，主要是偏好反馈而非命令 benchmark** | 无基础 LLM 大规模微调；memory/reflection 在线更新 | 具体 backbone 本次未可靠核实 | Highway-env；safety/efficiency/style adaptation | 论文称将发布；**实见公开 repo，但 README 表示仍在整理** citeturn307398search1turn307398academia4turn683687search3 |
| **SanDRA: Safe Large-Language-Model-Based Decision Making for Automated Vehicles Using Reachability Analysis** — Yuanfei Lin, 2026 | **已发表，IEEE T-ITS Early Access 2026-08-03**；arXiv:2510.06717；DOI 10.1109/TITS.2026.3713120 | a, f：LLM proposal/ranking + temporal logic + reachability verification | 否 | 比较 off-the-shelf 与 fine-tuned LLM | 多种 LLM | Highway-env；安全可达性、任务性能 | 声称公开 / **实见 CommonRoad/SanDRA 仓库** citeturn307398search2turn307398academia6turn683687search4 |
| **C-TRAIL: A Commonsense World Framework for Trajectory Planning in Autonomous Driving** — Zhihong Cui, 2026 | **已发表，IEEE TVT 2026**；arXiv:2603.29908；DOI 10.1109/TVT.2026.3682668 | e, h：LLM commonsense relation prior + trust + MCTS | 否 | planner/其他模块训练；LLM 非主要微调对象 | 型号未从一手摘要核实 | Highway-env 四场景 + highD/rounD | 论文声称代码可用；**实见 GitHub 仅 README/LICENSE，未见实现文件** citeturn632919search0turn632919academia6turn632919search1 |
| **SEDM: A Safety-Enhanced Decision-Making Framework for Autonomous Driving by Integrating Large Language Models and XGBoost** — Jun Li, 2026 | **已发表，IET ITS 2026**；DOI 10.1049/itr2.70178 | a, f：LoRA LLM 决策 + XGBoost shield | 否 | **ChatGLM3-6B LoRA + XGBoost**；**10,000** 专家 state-action 样本用于 LLM，安全 shield 另含危险样本；见 §4.2 | **ChatGLM3-6B** | Highway-env + merge-v0；SR、latency、速度、LCP/TP/SKP；Tables 1–3，Figs. 8–11 | 未看到官方代码树 citeturn116598view0turn916061search2 |
| **PhyZero: Physics-Grounded Zero-Shot Driving Agent** — Jiaheng Sun, 2026 | **已发表，CCDC 2026**；DOI 10.1109/CCDC69976.2026.11559983 | e, f, h：LLM action prior + physics-grounded MCTS | 否 | **training-free / zero-shot** | 型号未可靠核实 | Highway-env | 代码未看到 citeturn882491search4turn882491search5 |
| **LA-RL: Language Action-guided Reinforcement Learning with Safety Guarantees for Autonomous Highway Driving** — Yiming Shu, 2025 | **仅预印本**；arXiv:2512.05686 | e, f：language-action backbone 嵌入 actor-critic + MPC/DCBF safety | 否 | **SmolLM2-135M-Instruct 最后一层解冻，PPO；40,000 timesteps** | SmolLM2-135M-Instruct | **明确为 Highway-env `highway-v0`** | 项目/README 可见；**实见 repo 主要是 README/assets，未见实现源码** citeturn140331view0turn306303view1turn263437search0 |
| **GAPL: Grounded Action-effect Policy Learning for LLM-Based Trajectory Planning** — Zhihong Cui, 2026 | **仅预印本**；arXiv:2608.18254 | e, h：LLM action-effect evaluator + simulator grounding + distillation → PPO | 否 | PPO / distiller 训练 | LLM 型号未核实 | Highway-env 四场景 | 代码未看到 citeturn632919academia7 |
| **SARAD: LLM-Based Safety-Aware Hybrid Reinforcement Learning with Collision Prediction for Autonomous Driving** — Kangyu Wu, 2026 | **仅预印本**；arXiv:2605.28583 | e, f：RAG-LLM 引导探索 + collision predictor | 否 | RL 与碰撞预测模块训练 | 未可靠核实 | Highway-Env | 代码未看到 citeturn606724academia7 |
| **When Does Experience Memory Help Closed-Loop LLM Driving Agents? A Controlled Evaluation with Resampled Warmup Pools, Token-Matched Fillers, and Audited Baselines** — Yingxin Jia, 2026 | **仅预印本**；arXiv:2610.27714 | a, h：对 DiLu/RESPOND 型 memory 的受控检验 | 否 | 无基础模型训练；受控 memory 比较 | **gpt-4o-mini** 为关键实验模型 | HighwayEnv，1 Hz 闭环；memory/no-memory/token-matched controls | 论文称提供测试框架；本次未核实 repo | citeturn486763academia9 |
| **ConsciousDriver: A Context-Aware Multimodal Personalized Autonomous Driving System** — Noah Fang, 2026 | **仅预印本，未同行评审**；Preprints.org；DOI 10.20944/preprints202601.1454.v1 | a, c：context-aware personalized MLLM | **是**：驾驶风格与持续偏好 | MLLM personalization / soft prompt/LoRA | Vicuna/视觉编码器系，具体版本以预印本为准 | 扩展 PAD-Highway；约 250 h 数据 | 代码未看到 citeturn606724search5turn606724search8 |
| **LLM-guided deep reinforcement learning with contrastive safety regularization for autonomous driving** — Haochen Ren, 2026 | **已发表，Discover Artificial Intelligence**；DOI 10.1007/s44163-025-00812-w | e, f：LLM safety arbitration + replay regularization | 否 | DQN/安全正则训练；LLM 辅助判别 | 型号未从可访问主文可靠核实 | Highway-env | 代码未看到 citeturn814145view0turn854011search3 |
| **Retrieval-Augmented Large Language Model Decision-Making for Autonomous Driving Guided by Chinese Philosophical Wisdom** — Xiaojun Bi, 2026 | **仅预印本**；arXiv:2610.03948 | a, h：RAG + value/commonsense prior | 否；价值原则由系统提供，不是用户指令 benchmark | 无明确基础模型训练 | 未核实 | Highway-env multilane | 代码未看到 citeturn604291academia9 |
| **DuSA: Dual-loop self-learning framework for autonomous driving with LLM-guided reinforcement learning** — Jinchang Xu, 2026 | **已发表，Knowledge-Based Systems 343:116002**；DOI 10.1016/j.knosys.2026.116002 | e, f：LLM 异步生成/优化 safety filter，filter 再指导 DQN | 否 | DQN + policy distillation；LLM safety-filter loop | 型号从可访问正文片段未核实 | **custom platform built on Highway-Env**；ramp merge 等 | 代码未看到 citeturn582189search1turn582189search2turn132438search0 |
| **REINS: A Self-Evolving Agent Harness for Real-Time Trajectory Planning** — Zhihong Cui et al., 2026 | **已接收，NeurIPS 2026**；本次未找到可确认 DOI/arXiv ID | a, f, h：novel-scene LLM、grounding、verification、memory consolidation | 否 | 不更新 LLM 权重；经验库自演化 | 具体型号未核实 | Highway-env highway/merge/roundabout/intersection + highD/rounD | 声称公开 / **实见 GitHub 项目与实现说明** citeturn518104search0turn518104search1turn518104search2 |

有一个需要特别排除的“看起来很像”的条目：**HighwayLLM: Decision-Making and Navigation in Highway Driving with RL-Informed Language Model** 虽然标题含 *Highway*，但论文正文说明实验是“基于真实交通数据的实时仿真”，而不是 Edouard Leurent 的 Highway-env；因此我**没有**把它计入上述版图。citeturn582189search4

按上表进行多标签计数，我得到的“研究占位图”是：**(a) 逐步决策 15 篇；(b) 低频策略代码/程序 3 篇；(c) 人类语言指令/偏好直接进入驾驶 agent 约 6 篇；(d) 奖励设计 3 篇；(e) 给 RL/规划器提供先验 12 篇；(f) 安全过滤/验证 12 篇；(g) 多智能体协同 3 篇；(h) 记忆、反思、知识、对抗场景等其他作用 15 篇。**这是多标签计数，不能相加得到论文总数；而且 c 类中 DiLu 只是**支持** human intention、RESPOND 主要是偏好反馈，若只计算“有明确指令评测”的工作，数量会降到 4 篇左右。【推断，分类依据为上表方法描述】citeturn916061search7turn307398search1

## 指令驱动工作与覆盖矩阵

### 逐篇核查

**Receive, Reason, and React** 是 LaMPilot 之外最值得保留的指令研究。【原文】论文把语言命令直接送给 LLM，并在 HighwayEnv 里分别考察了 overtaking 和 merging；其中有用户要求超车、但场景安全条件不同的实验，以及 “more aggressively / conservatively” 这类驾驶风格命令。Table I 的评价量不是一个抽象的“instruction accuracy”，而是车辆行为指标，包括加速度、转向、速度、最小间距、完成时间和换道行为，因此“正确执行”主要通过**行为是否与命令方向一致且保持安全**判断。citeturn352544search0turn352544search7

【推断】它确实提供了近似“同环境、换 command/style”的对照，尤其 merging 部分比较 no-query / aggressive / conservative，但我没有找到论文把它设计成严格的“固定随机种子、只替换语言字符串”的 paired counterfactual protocol。它**没有**报告同义改写一致性；对不安全 overtaking，agent 能选择不执行，因此可视为测试了“拒绝危险命令”的最小实例，但论文没有建立独立的 refusal/wait/clarification accuracy 指标。citeturn352544search7

**LaMPilot** 是目前最系统化的工作。【原文】LaMPilot-Bench 被定义为用于评测 AD agent **instruction-following capabilities** 的 benchmark；4,900 个 semi-human-annotated traffic scenes 中，论文声明有 **500 个 test split 样本**。指令覆盖 **speed control、following distance、lane change、overtaking、intersection routing、pull over**；当前仓库还把这些任务明确拆成 evaluator。citeturn916061search8turn916061search3

LaMPilot 对“正确执行”的判据很具体：除任务目标外，还要求 **无碰撞、在时间限制内完成**；lane-change 等任务还有目标 lane/heading 条件。最终报告 completion、collision、TTC、Speed Variance、Time Efficiency 以及合成 Driving Score。citeturn105616view0turn105616view1

它的一个重要细节是，**生成的程序可以自行等待条件成熟**。论文示例中的 overtaking policy 会先检测目标/车道可用性，不满足条件时返回或继续 autopilot，因此从系统能力看具备“temporarily infeasible → wait”的机制；但【推断】benchmark 没有把“等待得对不对”拆成独立指令类型或独立指标。同样，论文没有建立“同一句话的若干同义改写”一致性测试，也没有 ambiguity/clarification benchmark。citeturn892311view1

**PADriver** 的核心语言输入是个性化驾驶 prompt，而不是路线任务式 command。【原文】PAD-Highway 包含不同个性化模式，公开版本明确区分 slow / normal / fast 等偏好；MLLM 根据连续视觉/环境输入和 personalized text prompt 产生行为。它用安全、效率和行为风格指标判断是否实现个性化，而不是给一句 instruction 一个 exact-match label。没有找到严格 paired “同场景只换 prompt”、同义改写一致性、冲突命令拒绝或澄清测试。citeturn676860search5turn307398academia3

**ConsciousDriver** 延续 PADriver 的方向，把 preference prompt 做得更 context-aware、持续化；例如偏好安全间距、避免激烈加速等可以贯穿一段驾驶过程。【原文】它仍属于 2026 年 Preprints.org 预印本，不能与已同行评审工作等量看待。没有找到 ambiguity / paraphrase / refusal 专门 benchmark。citeturn606724search5turn606724search8

**RESPOND** 中的人类输入更接近“在线偏好反馈”：系统把反馈写入 pattern/memory，并让驾驶行为逐渐向指定风格适应。【推断】因此它属于“人类偏好进入闭环 agent”，但不是 LaMPilot 式“一条自然语言 command → 判断是否完成任务”的 benchmark；我没有发现同义改写、歧义、澄清或严格 paired counterfactual 测试。citeturn307398search1

**DiLu** 需要单独区分“能力”和“实验”。【原文】附录写得非常明确：*“The driving intention can be input by humans to modify the vehicle’s behavior”*，但默认 intention 是安全驾驶、避免碰撞。因此它是“人可以给 driving intention”的系统，却**没有把多种自然语言用户指令作为正式实验变量进行系统评测**。citeturn916061search7

**Human-centric Reward Optimization** 也接受自然语言偏好，但语言并不直接成为在线驾驶 command。【原文】instruction + dynamic environment description 输入 GPT-3.5-turbo-1106，LLM 再产生/塑造 reward，DQN 按 reward 学习。因此它是 Q2 的“人类偏好输入”相关工作，但在角色分类里我把它放入 d/e，而不是把它等同于 LaMPilot 的 c 类。citeturn582189academia6turn116598view4

### 指令类型覆盖矩阵

符号说明：**●** = 有明确实验；**△** = 系统具备机制或间接涉及，但不是专门 benchmark；**—** = 未找到。

| 指令/偏好类型 | Receive, Reason, React | LaMPilot | PADriver | ConsciousDriver | RESPOND | DiLu | Human-centric Reward |
|---|---:|---:|---:|---:|---:|---:|---:|
| 显式机动：变道、超车、调速等 | ● | **●** | △ | △ | — | △ | — |
| 驾驶风格/偏好 | **●** | — | **●** | **●** | **●** | △ | **●** |
| 隐含意图 | — | — | △ | △ | △ | △ | △ |
| 歧义指令 | — | — | — | — | — | — | — |
| 与交通规则/安全冲突的指令 | **●：不安全超车请求** | △：程序含安全条件，但无冲突集 | — | — | — | — | — |
| 暂时不可执行指令 | — | △：程序可等待条件 | — | — | — | — | — |
| 多步、条件、持续约束 | — | △：生成程序本身可条件化/持续执行 | △ | **△/●：持续偏好** | △ | △ | — |
| “同场景只改 instruction”的严格 paired 测试 | △ | **未找到** | **未找到** | **未找到** | **未找到** | **未找到** | **未找到** |
| 同义改写一致性 | **未找到** | **未找到** | **未找到** | **未找到** | **未找到** | **未找到** | **未找到** |
| 拒绝危险命令 | **●，有限案例** | △ | — | — | — | — | — |
| 等待正确时机 | — | △，机制存在但未单独评分 | — | — | — | — | — |
| 主动澄清 | **未找到** | **未找到** | **未找到** | **未找到** | **未找到** | **未找到** | **未找到** |

这里对 Q6 可以给出较严格的空白声明：

- **隐含意图：未找到**专门 Highway-env benchmark。检索词包括 `"Highway-env" LLM implicit intent driving instruction`、`HighwayEnv language model implied intent autonomous driving`、`LaMPilot implicit instruction`。
- **歧义指令：未找到**。检索词包括 `"Highway-env" LLM ambiguous instruction autonomous driving`、`LaMPilot ambiguity ambiguous command`、`PAD-Highway ambiguous prompt`。
- **同义改写一致性：未找到**。检索词包括 `"LaMPilot-Bench" paraphrase synonym consistency`、`HighwayEnv LLM instruction paraphrase robustness`、`PADriver paraphrase prompt`。
- **暂时不可执行指令的专门评测：未找到**。LaMPilot 程序能等待，但这不是独立 benchmark category。检索词包括 `HighwayEnv LLM impossible instruction wait`、`temporarily infeasible driving command LLM HighwayEnv`、`LaMPilot wait unsafe instruction`。
- **需要主动澄清的命令：未找到**。检索词包括 `HighwayEnv LLM clarification driving instruction`、`LaMPilot clarify ambiguous command`。
- **复杂多步/条件自然语言约束的专门 benchmark：未找到**。检索词包括 `LaMPilot multi-step conditional instruction`、`Highway-env LLM persistent constraint driving language`、`compound driving instruction HighwayEnv LLM`。
- **与安全冲突的指令并非空白**：`Receive, Reason, and React` 的 unsafe-overtaking case 是我找到的明确实例；但它还远不是一个系统性的 adversarial-instruction benchmark。citeturn352544search7

## LaMPilot-Bench 的后续使用情况

LaMPilot 原论文的基准规模有一个容易误读、也值得特别记录的问题。【原文】CVPR 正文写明 **4,900 个 scenes，500 个样本划为 test set**。citeturn916061search8 但 Table 3 中 completion/collision 的许多百分比——例如 20.4%、35.7%、40.8%、72.4%、74.5%——以约 **1.02 个百分点**为最小步长；`1/98 ≈ 1.0204%`。【推断】因此论文 Table 3 的实际跑分极可能基于 **98 个实例**而非完整 500 test split。当前官方仓库也保留了与这一实验脚本/评估设置相对应的实现。这个“500 是 test split、Table 3 看起来是 98-run”应当在引用 LaMPilot 数字时明确区分，不能把两者混成一个样本量。citeturn669795view0turn916061search3

原论文 Table 3 的核心数字如下；这些都是**论文 Table 3**，不是我从二手博客拼出来的结果：0-shot completion 分别为 Llama 2 **20.4%**、PaLM 2 **35.7%**、ChatGPT **40.8%**、GPT-4 **72.4%**、GPT-4 Turbo **74.5%**；3-shot 中 GPT-4 为 **84.7% completion / 55.9 Driving Score**，GPT-4 Turbo 为 **80.6% / 52.6**；human-feedback setting 中 GPT-4 为 **92.7% / 64.0**，GPT-4 Turbo 为 **87.3% / 60.5**。论文对应页还说明 human-feedback policy repository 对每种方法使用 **100 个随机的非测试样本**，且不是参数微调。citeturn669795view0turn105616view1

模型设置也可以从论文实验页直接核实：Llama 2 **70B-chat**、PaLM 2 **code-bison**、ChatGPT **gpt-3.5-turbo**、GPT-4，以及 GPT-4 Turbo **gpt-4-1106-preview**。citeturn105616view1

我专门按用户建议对 DiLu 和 LaMPilot 做了前向引用式检索，但截至本次检索，**没有核实到第二篇独立论文在 LaMPilot-Bench 上以可追溯表格重新跑一整套 500/98 样本结果**。一些后续综述/综合 benchmark 工作提到或纳入 LaMPilot-Bench，例如 2026 年的 *LLM4AD: Large Language Models for Autonomous Driving—Concept, Review, Benchmark, Experiments, and Future Trends*；但是我没有取得足够的一手表格证据来证明它报告的是一套新的、独立重跑的 LaMPilot 数字，而不是引用/整合原论文结果，因此**不把它计为“已核实的独立 LaMPilot-Bench 后续跑分”**。citeturn512782search3turn486763search5

同样，**未核实到后续论文正式扩展 LaMPilot-Bench 的 instruction taxonomy**。当前官方仓库现在描述为 32 类/配置化 driving scenarios、总计 4,900 test cases，并增加/维护 `DTHighwayEnv`、`DTIntersectionEnv`、`RampMergeEnv` 等实现以及 speed、distance、lane change、overtake、intersection、pull-over evaluators；这些属于 LaMPilot 项目自身持续维护，不能自动当成另一篇论文提出的 benchmark extension。citeturn916061search3turn916061search5

与此相对，**PAD-Highway 是另一套 Highway-env 派生 benchmark，不是 LaMPilot-Bench extension**；它针对个性化 MLLM 驾驶，研究问题不同。citeturn307398academia3

## 对 Highway-env 的明确评价

LaMPilot 对“为什么选 HighwayEnv”给的是正面理由。论文 §4.1 原文称：

> “HighwayEnv offers various driving models and simulates realistic multi-vehicle interactions.”

随后说明他们在此基础上增加适合 LLM agent 的接口和自定义 intersection。也就是说，作者看中的是**可控的交互交通、可编程高层动作接口和易于构造多任务场景**，而不是感知保真度。citeturn916061search8

LORD 则给出了我找到的最直接的视觉保真度批评：

> “Highway-env provides a simplified visualization where all vehicles are depicted as rectangles.”

论文紧接着指出这种渲染“很可能”落在大预训练视觉模型的训练分布之外，因此作者给矩形车辆替换更接近真实车的纹理，而不是直接把原始 Highway-env render 喂给 CLIP/S3D。这是一个非常具体的 **simulator rendering → pretrained-model distribution shift** 问题。citeturn565815view0

SEDM 一方面明确解释了选择原因：

> “It supports configurable traffic density and vehicle counts, provides kinematic vehicle dynamics models that approximate real-world behaviour…”

并指出还带有内建可视化，适合可控实验。citeturn116598view0

但 SEDM 在结论中也非常明确地承认外部有效性限制：

> “our evaluation is confined to the highway-env simulator, which features structured road layouts and normal traffic dynamics.”

作者继续说明这不能覆盖真实驾驶中的城市路口、行人、恶劣天气；而且系统假设能直接得到**精确位置、速度和 lane ID**，绕过了原始摄像头/LiDAR 感知、遮挡、部分可观测性和感知噪声。因此，对 Highway-env 最准确的概括不是“它不真实所以没价值”，而是：**它很适合隔离和研究 tactical decision / language reasoning / safety logic，但几乎不测完整自动驾驶栈中的 perception 和 sim-to-real 问题。**最后一句是【推断】，前述限制为论文【原文】。citeturn116598view0

DiLu 的设置也印证这一点。【原文】其 Highway-env 实验“directly obtain vehicle information from the underlying simulation”，输入的是当前帧车辆位置、速度、加速度；这不是 perception-from-pixels。citeturn916061search7

## 检索过程、边界与未能核实的内容

检索首先以用户给定条目为种子，组合了 `"Highway-env" / "HighwayEnv" + LLM / large language model / VLM / MLLM / autonomous driving / reward / safety / reinforcement learning / instruction`；随后以 **DiLu、LaMPilot / LaMPilot-Bench** 为前向引用锚点，搜索标题引用、后续 comparison、benchmark、memory、safety、collaborative driving、reward-design、rule-generation 等方向。为了 Q2/Q6，另做了 `ambiguous instruction`、`implicit intent`、`paraphrase/synonym consistency`、`unsafe/conflicting instruction`、`wait/impossible instruction`、`clarification`、`multi-step/conditional/persistent constraint` 等定向检索。LaMPilot、DiLu、SEDM、LORD 等优先使用论文正文、CVF/IEEE/Wiley/arXiv 官方页面；代码状态则尽量打开 GitHub 项目而不是相信论文一句“code available”。citeturn916061search8turn916061search0turn116598view0

对 PDF 的关键页我实际检查了 LaMPilot Table 2、实验设定和 Table 3；这也是为什么上面对 LaMPilot 的数字只写有表号、且能区分论文声明的 **500 test split** 与 Table 3 显示出的 **98-sample 痕迹**。citeturn105616view0turn105616view1turn669795view0 LORD 的正文可解析，但网页端 PDF screenshot 请求被源站拒绝；因此这里只使用能够从解析正文核实的短引文，不声称检查了其页面视觉版式。citeturn565815view0

几个边界判断需要保留。第一，**HighwayLLM 被排除**，因为不是 Leurent Highway-env。第二，纯 Highway-env RL、没有 LLM 实质参与的不纳入。第三，凡是“论文只引用 Highway-env、但实际实验平台无法确认”的条目不主动补入。第四，AgentsCoDriver、ADRD 一类工作的 Highway-env 证据虽然能够通过论文索引/项目资料核对，但公开一手正文的可访问性弱于 LaMPilot/SEDM，因此我没有给出超出可验证材料的细粒度训练数字。第五，**REINS** 的 NeurIPS 2026 accepted 状态可从作者/项目页核实，但本次没有找到可确认的 arXiv ID 或 DOI，因此保留“未找到”，不猜编号。citeturn582189search4turn518104search2

代码方面尤其需要警惕“paper says open-source”和“仓库里真的有代码”的差别：DiLu、LaMPilot、CoDrivingLLM、CRITICAL、SanDRA 等我确实看到了实现目录；C-TRAIL 的公开仓库在本次抓取时主要只看到 README/LICENSE；LA-RL 也主要是 README/assets；RESPOND 的仓库公开但 README 明示代码仍在整理。这些状态是截至 **2026-11-07** 的检索快照，以后可能变化。citeturn916061search0turn916061search5turn676860search3turn606724search3turn632919search1turn263437search0turn683687search3

## 参考文献

以下只写本报告纳入或用于边界判断的主要条目；“—”表示本次没有可靠找到相应标识或代码地址。

**Drive Like a Human: Rethinking Autonomous Driving with Large Language Models** | 2024 | WACV Workshops | DOI 10.1109/WACVW60836.2024.00102 | `https://github.com/PJLab-ADG/DriveLikeAHuman` citeturn606724search0turn712321search1

**Receive, Reason, and React: Drive as You Say with Large Language Models in Autonomous Vehicles** | 2024 | IEEE Intelligent Transportation Systems Magazine | DOI 10.1109/MITS.2024.3381793 | 项目页见论文记录，代码树本次未确认 citeturn352544search0turn352544search2

**DiLu: A Knowledge-Driven Approach to Autonomous Driving with Large Language Models** | 2024 | ICLR | arXiv:2309.16292 | `https://github.com/PJLab-ADG/DiLu` citeturn916061search0

**LaMPilot: An Open Benchmark Dataset for Autonomous Driving with Language Model Programs** | 2024 | CVPR | arXiv:2312.04372；DOI 10.1109/CVPR52733.2024.01434 | `https://github.com/PurdueDigitalTwin/LaMPilot` citeturn916061search6turn916061search5

**Human-centric Reward Optimization for Reinforcement Learning-based Automated Driving using Large Language Models** | 2024 | arXiv preprint | arXiv:2405.04135 | 论文称源码/数据可用，仓库本次未确认 citeturn582189academia6

**Generating and Evolving Reward Functions for Highway Driving with Large Language Models** | 2024 | IEEE ITSC | arXiv:2406.10540；DOI 10.1109/ITSC58415.2024.10919977 | — citeturn224955academia2turn148788search4

**LORD: Large Models Based Opposite Reward Design for Autonomous Driving** | 2025 | WACV | arXiv:2403.18965；DOI 10.1109/WACV61041.2025.00496 | — citeturn512782search5turn512782search8

**Hybrid-Driving: An Autonomous Driving Decision Framework Integrating Large Language Models, Knowledge Graphs and Driving Rules** | 2025 | AAAI | DOI 10.1609/aaai.v39i1.32066 | — citeturn224955search1

**KoMA: Knowledge-Driven Multi-Agent Framework for Autonomous Driving With Large Language Models** | 2024/2025 | IEEE Transactions on Intelligent Vehicles | DOI 10.1109/TIV.2024.3488793 | 项目页提供代码入口 citeturn882491search1turn882491search0

**Towards Interactive and Learnable Cooperative Driving Automation: a Large Language Model-Driven Decision-Making Framework** | 2025 | IEEE Transactions on Vehicular Technology | arXiv:2409.12812；DOI 10.1109/TVT.2025.3552922 | 公开 GitHub 仓库已实见 citeturn676860search2turn676860search3

**AgentsCoDriver: Large Language Model Empowered Collaborative Driving with Lifelong Learning** | 2024 | arXiv preprint | arXiv:2404.06345 | 本次未确认 citeturn854011academia9

**Enhancing Autonomous Vehicle Training with Language Model Integration and Critical Scenario Generation** | 2024 | arXiv preprint | arXiv:2404.08570 | 公开 GitHub 仓库已实见 citeturn606724search6turn606724search3

**PADriver: Towards Personalized Autonomous Driving** | 2025 | IJCNN | arXiv:2505.05240；DOI 10.1109/IJCNN64981.2025.11228638 | — citeturn307398search0turn307398academia3

**Large language model guided deep reinforcement learning for safe autonomous vehicle decision making** | 2026 | Transportation Research Part C | arXiv:2412.18511；DOI 10.1016/j.trc.2025.105511 | 项目页声称代码 citeturn604291search0turn604291academia8

**ADRD: LLM-Driven Autonomous Driving Based on Rule-based Decision Systems** | 2025 | arXiv preprint | arXiv:2506.14299 | — citeturn521830academia9

**BladeRunner-AD: Adversarial Co-evolution of Robust and Interpretable Driving Policies via LLM Agent Games** | 2025 | IEEE MESA | DOI 10.1109/MESA68091.2025.11278881 | — citeturn582189search0

**RESPOND: Risk-Enhanced Structured Pattern for LLM-driven Online Node-level Decision-making in Autonomous Driving** | 2026 | Communications in Transportation Research | arXiv:2512.20179；DOI 10.26599/COMMTR.2026.9640037 | `https://github.com/gisgrid/RESPOND`，仓库仍在整理 citeturn307398search1turn683687search3

**SanDRA: Safe Large-Language-Model-Based Decision Making for Automated Vehicles Using Reachability Analysis** | 2026 | IEEE Transactions on Intelligent Transportation Systems, Early Access | arXiv:2510.06717；DOI 10.1109/TITS.2026.3713120 | `https://github.com/CommonRoad/SanDRA` citeturn307398search2turn683687search4

**C-TRAIL: A Commonsense World Framework for Trajectory Planning in Autonomous Driving** | 2026 | IEEE Transactions on Vehicular Technology | arXiv:2603.29908；DOI 10.1109/TVT.2026.3682668 | 论文所给 GitHub；本次实见仅 README/LICENSE citeturn632919search0turn632919search1

**SEDM: A Safety-Enhanced Decision-Making Framework for Autonomous Driving by Integrating Large Language Models and XGBoost** | 2026 | IET Intelligent Transport Systems | DOI 10.1049/itr2.70178 | — citeturn116598view0

**PhyZero: Physics-Grounded Zero-Shot Driving Agent** | 2026 | CCDC | DOI 10.1109/CCDC69976.2026.11559983 | — citeturn882491search4turn882491search5

**LA-RL: Language Action-guided Reinforcement Learning with Safety Guarantees for Autonomous Highway Driving** | 2025 | arXiv preprint | arXiv:2512.05686 | 公开 repo；本次未见核心实现源码 citeturn140331view0turn263437search0

**GAPL: Grounded Action-effect Policy Learning for LLM-Based Trajectory Planning** | 2026 | arXiv preprint | arXiv:2608.18254 | — citeturn632919academia7

**SARAD: LLM-Based Safety-Aware Hybrid Reinforcement Learning with Collision Prediction for Autonomous Driving** | 2026 | arXiv preprint | arXiv:2605.28583 | — citeturn606724academia7

**When Does Experience Memory Help Closed-Loop LLM Driving Agents? A Controlled Evaluation with Resampled Warmup Pools, Token-Matched Fillers, and Audited Baselines** | 2026 | arXiv preprint | arXiv:2610.27714 | 本次未确认 citeturn486763academia9

**ConsciousDriver: A Context-Aware Multimodal Personalized Autonomous Driving System** | 2026 | Preprints.org，未同行评审 | DOI 10.20944/preprints202601.1454.v1 | — citeturn606724search5

**LLM-guided deep reinforcement learning with contrastive safety regularization for autonomous driving** | 2026 | Discover Artificial Intelligence | DOI 10.1007/s44163-025-00812-w | — citeturn814145view0

**Retrieval-Augmented Large Language Model Decision-Making for Autonomous Driving Guided by Chinese Philosophical Wisdom** | 2026 | arXiv preprint | arXiv:2610.03948 | — citeturn604291academia9

**DuSA: Dual-loop self-learning framework for autonomous driving with LLM-guided reinforcement learning** | 2026 | Knowledge-Based Systems 343:116002 | DOI 10.1016/j.knosys.2026.116002 | — citeturn582189search2

**REINS: A Self-Evolving Agent Harness for Real-Time Trajectory Planning** | 2026 | NeurIPS 2026，已接收 | arXiv/DOI：本次未找到可确认编号 | 公开 GitHub 项目已实见 citeturn518104search0turn518104search2
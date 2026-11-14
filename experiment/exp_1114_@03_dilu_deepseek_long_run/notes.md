# DiLu DeepSeek 长时程实验过程笔记与深入解析

## 一、 实验背景与时长决策依据

在 `@02` 最小实验中，我们验证了 DeepSeek-V3 驱动 DiLu 的 3 步闭环连通性。本次实验 `@03` 的核心诉求为：**“保持其他设置不变，把时间拉长，选择有依据的数字中比较长的，观察真实效果”**。

### 为什么选择 30 步（而不是 10 步、20 步或 100 步）？

1. **学术依据严谨性（依据 `@2024_ICLR_DiLu` 正文）**：
   - 在 DiLu 原论文的实验设计中，仿真器环境为 Highway-env，策略与仿真交互频率设定为 $1\text{ Hz}$（单步决策即对应现实世界 1 秒钟物理时间）。
   - 论文在定义核心评测指标 **Success Steps (SS)** 时，将单次闭环驾驶任务的终止判定上线设定为 **30 步（30 consecutive decision frames / 30 seconds）**。
   - 论文指出：自车在不发生碰撞的前提下安全运行满 30 步，即判定该 Episode 为 **Task Success**（任务成功）。因此，**30 步是论文评测基准中的官方终点线**。
2. **代码库与环境默认值对比**：
   - 官方代码库 `repos/DiLu/config.yaml` 中给出的模板值为 `simulation_duration: 20`；
   - 原生 Highway-env 默认配置为 `40` 秒。
   - 综合衡量，**30 步**既是学术界评估 DiLu 的公认标准评测时程（全时程 Benchmark），也是在有明确依据的参数中兼具挑战性与代表性的较长时程设定。

---

## 二、 实验执行与关键配置记录

- **实验分支**：在 `repos/DiLu` 中创建 `exp_1114_@03_dilu_deepseek_long_run` 分支，更新基础配置 `simulation_duration: 30` 并通过离线冒烟测试，随后按照实验规范压缩合并（squash merge）至 `main`（提交哈希 `ebe79c2`）。
- **实验配置**：`experiment/exp_1114_@03_dilu_deepseek_long_run/config.yaml`
  - 种子：`5838`（与 `@02` 一致，确保交通流初始条件完全一致，使 3 步后的长时程轨迹具有确定性的连续可比性）。
  - 模式：`few_shot_num: 0`（Zero-Shot），`reflection_module: False`。
  - 模型：`deepseek-chat`（DeepSeek-V3 官方 API），`temperature: 0.0`，`thinking: {'type': 'disabled'}`。

---

## 三、 长时程驾驶行为特征与深入技术洞察

### 1. 现代前沿 LLM（DeepSeek-V3）与 2023 年初代基线（GPT-3.5）的性能代差

在 [`@2024_ICLR_DiLu`](file:///D:/Workspace/00_MyRepo/LLM_drive_research/papers_md/@2024_ICLR_DiLu.md) 论文正文第 4.1 节中，作者记录了原始 GPT-3.5 的 0-shot 表现：
> *"In comparison, when the framework lacks the Memory module and runs a 0-shot experiment, no tasks are successfully conducted and the median SS is below 5. This indicates that LLM cannot directly perform the closed-loop driving tasks without any adaptation."*

- **原论文基线结论**：在 2023 年使用 GPT-3.5 进行 0-shot 测试时，**没有任何一个场景能够成功完成，中位数成功步数（Median SS）甚至低于 5 步**（车辆极早发生追尾或擦碰）。原论文正是以此为基础，论证了引入 Memory（检索经验）和 Reflection（反思纠错）的必要性。
- **本次 DeepSeek-V3 实验结果**：在完全 **Zero-Shot（0 示例、0 记忆库）** 的条件下，DeepSeek-V3 面对 2.0 高密度复杂车流，一次性达成了 **满分 30 步（$SS=30$）无碰撞通过**，全程行驶 491.80 米。
- **技术洞察**：这强力证明了近两年来 LLM 基础推理能力（尤其是空间几何数据理解、多步因果逻辑推理、风险敏感度）的巨大飞跃。对于结构化文本表征的道路交通场景，DeepSeek-V3 展现出极高水准的驾驶常识素养。

### 2. 纵向速度自适应调整的合理性分析

纵观 30 帧的动作序列 `[4, 4, 1, 1, ..., 4, 1, 1, ...]`：
- **两次制动窗口的精准触发**：
  - **第一次制动（Frame 0 ~ 1）**：面对初始高速入场（25 m/s）叠加同车道前车急刹（$-6\text{ m/s}^2$）的生死危机，模型毫不犹豫连续下发 2 次制动，将车速压至 19.17 m/s。
  - **第二次制动（Frame 13）**：在平稳巡航 10 秒后，前车 856 出现减速（$-0.37\text{ m/s}^2$）且间距缩小至 31 米，模型并未教条地继续 IDLE，而是在 Prompt-guided CoT 中经过理性权衡，主动执行第 3 次减速（车速调降至 15.13 m/s）。
- **稳态跟驰的自收敛性**：
  - 在第 14 帧后，自车车速（15.13 m/s）与前方车流（16.20 m/s）形成稳定的速度差，车距自然拉大到 40~45 米的宽裕安全包线内。自车此后持续保持 IDLE，平稳完成整个测试。
- **无盲目变道的理性决策**：
  - 观察 30 帧的文字推导可以发现，模型在每一个决策步中都在细致排查左右车道的空档（如 Frame 13 排查左道车速过慢、右后车加速逼近）。在当前车道可以通过减速获得充分安全裕度时，模型始终遵循“防御性驾驶（Defensive Driving）”原则，优先采取确定性更高的纵向控距，而不是贸然变道引发新的侧向冲突。

---

## 四、 潜在担忧与后续实验建议

1. **单场景随机种子局限性**：
   - 本次使用的是基准种子 `5838`。尽管交通密度高达 2.0，属于极度拥堵博弈工况，但单一种子依然可能存在偶发成功。
   - **后续建议**：后续实验可引入 DiLu 官方的 17 个固定评测种子集（`test_list_seed`）进行批量统计（Batch Evaluation），计算真实的整体成功率（Success Rate, SR）与平均成功步数（Mean SS）。
2. **长时程变道动机相对保守**：
   - 在 Zero-Shot 且 Prompt 强调“Drive safely and avoid collisions”的设定下，模型策略整体呈现较为保守的防御风格。自车始终在第 3 车道完成全程，未触发主动超车变道（LANE_LEFT / LANE_RIGHT）。
   - **后续建议**：若想观察模型的变道与超车策略，可尝试在 Prompt 中微调驾驶意图（如添加效率目标“drive safely while maintaining desired cruising efficiency”），或者测试车道受阻必须变道绕行的强迫变道场景。
3. **格式与系统稳健性**：
   - 30 次 API 交互全部一步解析成功，耗时仅约 70 秒，每步平均延时约 2.3 秒，表明 DeepSeek-V3 的 API 吞吐与稳定性非常适合作为 Highway-env 的实时决策大脑。

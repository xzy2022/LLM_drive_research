# DiLu 最小实验过程笔记与深入解析

## 一、 核心概念辨析：提示词级思维链 (Prompt-guided CoT) vs 模型底层思考模式 (Thinking / Reasoning Mode)

针对用户关于“思维链”用词严谨性的疑问，特在此进行技术辨析与定义澄清：

1. **模型底层的思考模式（RL-based Thinking / Reasoning Mode / 推理等级）**：
   - **典型代表**：DeepSeek-R1、OpenAI o1 / o3 系列。
   - **机制**：通过大规模强化学习训练出的**内部隐藏推理机制**。API 层面会将这一思考过程存放在专用的 `reasoning_content`（或 `thinking` 块）中，独立于最终正文回复。
   - **本次实验状态**：**已显式禁用**（`thinking: {'type': 'disabled'}`）。本次调用的是标准对话模型 `deepseek-chat`（DeepSeek-V3），未启用底层 R1 风格的原生思考块。

2. **提示词引导的正文显式分析（Prompt-guided CoT, Chain-of-Thought）**：
   - **典型代表**：Wei et al. (2022) 提出的经典思维链方法，这也是 DiLu 论文（2023/2024 ICLR 原作者）设计时的时代背景与实现方式。
   - **机制**：通过 System Prompt 强制模型在生成最终答案前，必须在常规回复正文中输出 `<reasoning> ... </reasoning>`，显式写出中间推理步骤。
   - **本次实验状态**：**实际使用的正是这种模式**。模型不是“暗中思考后直接给答案”，而是在文本正文中先输出一段逐步排查逻辑，再输出动作代号。

> **规范定义**：后续记录中统一规范称为**“提示词引导的正文显式分析（Prompt-guided CoT）”**。

---

## 二、 逐帧输入与输出的完整对照报告（Frame 0 ~ 2）

### 1. Frame 0（初始高速跟车）：全量模板对照

#### 【输入 Prompt 提取自环境】
* **System Message**：定义成熟驾驶助手，要求输出 `<reasoning>` 并在末尾以 `Response to user:#### <Action_id>` 结尾。
* **Human Message 场景核心数据**：
  ```text
  You are driving on a road with 4 lanes, and you are currently driving in the third lane from the left.
  Your current position is `(363.46, 8.00)`, speed is 25.00 m/s, acceleration is 0.00 m/s^2.
  - Vehicle `920` is driving on the lane to your left and is ahead of you: Pos (373.11, 4.00), speed 22.10 m/s, acc 0.00 m/s^2.
  - Vehicle `304` is driving on the same lane as you and is ahead of you: Pos (382.31, 8.00), speed 21.41 m/s, acc 0.00 m/s^2.
  - Vehicle `160` is driving on the lane to your right and is ahead of you: Pos (402.44, 12.00), speed 21.56 m/s, acc 0.00 m/s^2.
  ```

#### 【DeepSeek 实际生成文本 Response】
```text
<reasoning>
I'm in the third lane from the left, traveling at 25 m/s. Vehicle 304 is directly ahead in my lane at 382.31 m, only about 19 m ahead, moving at 21.41 m/s — slower than me. I'm closing the gap quickly, so I need to either change lanes or decelerate.

Checking lane change options:
- Left lane: Vehicle 920 is at 373.11 m, ahead of me and slightly slower (22.10 m/s). It's close but there's a gap; however changing left would put me behind a slower vehicle.
- Right lane: Vehicle 160 is at 402.44 m, farther ahead, moving at 21.56 m/s. There's more space to the right.

The most immediate concern is the closing distance to vehicle 304. Decelerating is the safest, most direct action to avoid collision since I'm approaching a slower vehicle in my lane. A lane change could work but requires careful timing; deceleration is the safest immediate choice.
</reasoning>
####
Response to user:#### 4
```
* **Python 提取与执行**：切分取出最后的数字 `4` $\to$ 执行 `Deceleration`。

---

### 2. Frame 1（前车突发急刹）：简明输入输出对照

#### 【输入 Prompt 提取自环境】
* **自车瞬时状态**：第 3 车道，位置 $(386.89, 8.00)$，速度降至 $22.41\text{ m/s}$，加速度 $-1.00\text{ m/s}^2$。
* **周围车辆关键动态**：
  * **同道前车 304（急刹险情）**：位置 $(400.80, 8.71)$，**速度骤降至 $15.41\text{ m/s}$，加速度高达 $-6.00\text{ m/s}^2$**，间距被急剧压至 $13.91\text{ m}$！
  * **左道车辆 920**：位置 $(394.69, 4.00)$，速度 $20.95\text{ m/s}$（距自车仅 $7.8\text{ m}$，左变道空间不足）。
  * **右道车辆 160**：位置 $(421.22, 12.00)$，速度 $15.95\text{ m/s}$（也在减速 $-3.24\text{ m/s}^2$）。

#### 【DeepSeek 实际生成文本 Response】
```text
<reasoning>
I'm in the third lane from the left, traveling at 22.41 m/s with a deceleration of -1.00 m/s². Vehicle 304 is directly ahead in my lane at 400.80 m, only about 14 m ahead, moving at 15.41 m/s and decelerating hard at -6.00 m/s². This is a closing situation — I'm approaching a slower, braking vehicle in my lane.

Vehicle 920 is in the left lane ahead at 394.69 m, moving at 20.95 m/s. It's slightly ahead of me but the gap is small (~8 m), so changing left isn't clearly safe and wouldn't help much.

Vehicle 160 is in the right lane at 421.22 m, moving at 15.95 m/s and decelerating. Changing right would put me behind another slower vehicle.

The most pressing issue is the vehicle directly ahead in my lane (304) which is much slower and braking hard. I need to reduce speed to avoid collision. Deceleration is the safest immediate action.
</reasoning>

Response to user:#### 4
```
* **Python 提取与执行**：切分取出最后的数字 `4` $\to$ 连续执行第二轮 `Deceleration`。

---

### 3. Frame 2（前车变道让空，恢复巡航）：简明输入输出对照

#### 【输入 Prompt 提取自环境】
* **自车瞬时状态**：第 3 车道，位置 $(407.33, 8.00)$，车速安全平抑至 $19.17\text{ m/s}$，加速度 $-1.25\text{ m/s}^2$。
* **周围车辆关键动态**：
  * **原前车 304（已离开本道）**：变道移至右侧邻道，位置 $(413.95, 11.44)$，车速 $12.34\text{ m/s}$，不再威胁本车道。
  * **本车道新前车 432（安全开阔）**：位置 $(433.67, 8.00)$，车距拉大至 $26.34\text{ m}$，车速 $19.45\text{ m/s}$（略快于自车，距离持续拉大）。
  * **左道车辆 288**：位置 $(478.14, 4.00)$，远在 70 米外，无冲突。

#### 【DeepSeek 实际生成文本 Response】
```text
<reasoning>
I'm in the third lane from the left, moving at 19.17 m/s with a slight deceleration. Vehicle 432 is directly ahead in my lane at 433.67 m, moving at 19.45 m/s — slightly faster than me, so the gap is growing, not shrinking. That's fine.

Vehicle 304 is to my right, ahead, but slower (12.34 m/s) — no conflict since it's in a different lane.

Vehicle 288 is to my left, far ahead (478.14 m) and decelerating hard (-6.00 m/s^2) — it's slowing rapidly but it's in a different lane and far away.

The main consideration: my lane ahead is clear with a growing gap to vehicle 432. No need to change lanes. My current deceleration is mild and appropriate. Staying in lane with current speed is the safest choice.
</reasoning>

Response to user:#### 1
```
* **Python 提取与执行**：切分取出最后的数字 `1` $\to$ 执行 `IDLE`（保持当前车速与车道）。

---

## 三、 三帧全流程因果闭环总结

| 决策帧 | 自车车速 | 输入识别的核心特征 | 模型正文推导焦点 | 决策动作 | 物理结果 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Frame 0** | $25.00\text{ m/s}$ | 前车同道且比自车慢 $3.6\text{ m/s}$，间距仅 $18.8\text{ m}$ | 左右变道均不如减速直接安全 | `4 (Deceleration)` | 减速至 $22.41\text{ m/s}$ |
| **Frame 1** | $22.41\text{ m/s}$ | 前车急刹（$-6\text{ m/s}^2$），间距压至 $13.9\text{ m}$ 临界点 | 左道间隙仅 8 米不可变道，必须全力保底制动 | `4 (Deceleration)` | 减速至 $19.17\text{ m/s}$，防追尾 |
| **Frame 2** | $19.17\text{ m/s}$ | 前车右转离开，新前车在 $26.3\text{ m}$ 外且车速更快 | 前路已净空且新前车在拉开距离，无需变道或继续刹车 | `1 (IDLE)` | 恢复 $19.17\text{ m/s}$ 平稳巡航 |

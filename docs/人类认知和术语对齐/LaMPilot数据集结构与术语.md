# LaMPilot 数据集结构与术语

> 论文：`@2024_CVPR_LaMPilot-Bench`。
> 来源：合并自 `docs/LaMPilot数据集说明.md` 和 `experiment/exp_1107_@02_lampilot_deepseek_demo/实验情况说明.md`（2026-11-07）；数字已对照本地仓库 `repos/LaMPilot/projects/lampilot/` 的 `configs/DbLv1/*.json` 和 `dt/dbl.py` 复核。
> 论文结果和测试划分见 [LaMPilot测试划分与论文结果](LaMPilot测试划分与论文结果.md)。

## 1. 术语表（本项目统一用法）

```
任务类别（6）
 └─ 任务配置 JSON（32）
     └─ 场景（490）= 任务配置 + sX        ← 包含道路/车流设置、评测器、场景种子
         └─ 样本（4,900）= 场景 + cY       ← cY 是同一意图的 10 条指令改写之一
```

| 本项目术语 | 数量 | 编号形式 | 含义 | 论文 / 代码中的叫法 |
| --- | --- | --- | --- | --- |
| 任务类别 | 6 | Routing、Distance-related 等 | 论文 Table 2 的分类 | 论文：task category |
| 任务配置 | 32 | `dec_abs_dis25.json` | 一个官方 JSON 文件，对应一种带目标值的驾驶任务 | 代码：config |
| 场景 | 490 | `dec_abs_dis25_s1` | 任务配置 × 基础场景编号；一个初始交通状态加一个评测器 | **JSON 的 `samples` 数组元素、代码里的 `sample` 字段** |
| 基础场景编号 | 每个任务配置 10 / 20 / 50 个 | `s0`–`s9`、`s0`–`s19`、`s0`–`s49` | 场景在所属 JSON 内的序号 | 代码：`sample_idx` |
| 指令 | 每个任务配置 10 条 | `c0`–`c9` | 同一意图的 10 种自然语言说法（改写）；同一任务配置的所有场景共用这 10 条 | JSON：`commands` |
| 样本 | 4,900 | `dec_abs_dis25_s1_c0` | 场景 × 指令；评测的最小单位，一个样本 ID 对应一次运行 | 代码：`id` / `iid`；论文：traffic scenes / scenarios |
| 场景种子 | 每个场景 1 个 | `251`、`22567687678` | 场景 JSON 里的 `seed`，控制交通初始化；官方固定，不是样本 ID 的一部分 | JSON：`seed` |
| Demo 集 | 12 个样本 | 见第 5 节 | 官方固定的 12 个样本 | 代码：`DbLv1DemoDataset` |

### 易混点

1. **代码里的 `sample` 是场景（490 级），不是样本。** 本项目说“样本”一律指 4,900 级的样本 ID。
2. **论文里的 “4,900 traffic scenes” 就是 4,900 个样本。** 本项目的“场景”只指 490 级。
3. **三种“种子”要分开说：**
   - 场景种子：官方 JSON 固定，同一场景的 10 个样本共用。
   - 额外随机种子（重复次数）：我们自己为了多次重复实验而加的种子。实验 02 没有加。
   - 抽样种子：从数据集中随机抽样本时用的种子（例如平台探针的抽样）。

## 2. 32 个任务配置 JSON

| JSON 文件名前缀 | 中文 | JSON 个数 | 每个 JSON 的场景数 | 场景合计 |
| --- | --- | --- | --- | --- |
| `dec_abs_dis*`、`dec_rel_dis*`、`inc_abs_dis*`、`inc_rel_dis*`、`dec_abs_speed*`、`dec_rel_speed*`、`inc_abs_speed*`、`inc_rel_speed*` | 距离、速度控制 | 24 | 10 | 240 |
| `left_lc`、`right_lc`、`left_overtake`、`right_overtake`、`pull_over` | 左右变道、左右超车、靠边停车 | 5 | 20 | 100 |
| `turn_left`、`turn_right`、`go_straight` | 左转、右转、直行 | 3 | 50 | 150 |
| 合计 | | 32 | — | 490 |

命名规则：`dec` / `inc` = 减小 / 增大；`abs` / `rel` = 绝对目标 / 相对变化；`dis` / `speed` = 跟车距离 / 速度；末尾数字是目标值。例如 `dec_abs_dis25` 的指令是 “Decrease gap to 25 meters.”。

## 3. 任务类别与 JSON 的对应

| 任务类别（论文原文）¹ | 中文 | 对应 JSON（不含 `.json`）² | JSON 数² | 场景数² | 样本数¹ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Routing | 路线导航 | `go_straight`、`turn_left`、`turn_right` | 3 | 150 | 1,500 |
| Distance-related | 距离控制 | `dec_abs_dis*`、`dec_rel_dis*`、`inc_abs_dis*`、`inc_rel_dis*` | 12 | 120 | 1,200 |
| Speed-related | 速度控制 | `dec_abs_speed*`、`dec_rel_speed*`、`inc_abs_speed*`、`inc_rel_speed*` | 12 | 120 | 1,200 |
| Lane changing | 变道 | `left_lc`、`right_lc` | 2 | 40 | 400 |
| Overtaking | 超车 | `left_overtake`、`right_overtake` | 2 | 40 | 400 |
| Pulling over | 靠边停车 | `pull_over` | 1 | 20 | 200 |
| **合计** | **6 类** | | **32** | **490** | **4,900** |

¹ 论文直接报告：CVPR 2024 论文第 5 页 Table 2（Main statistics of the LaMPilot-Bench dataset）给出六类名称、各类数量（1,500 / 1,200 / 1,200 / 400 / 400 / 200）和总数 4,900。论文把总数称为 Total scenarios，按本项目术语就是 4,900 个样本。

² 根据仓库统计：官方 [config_list.txt](https://github.com/PurdueDigitalTwin/LaMPilot/blob/master/projects/lampilot/configs/DbLv1/config_list.txt)、各 JSON 的 `samples` 和 `commands` 数组，以及 [dbl.py](https://github.com/PurdueDigitalTwin/LaMPilot/blob/master/projects/lampilot/dt/dbl.py) 的展开逻辑。这些是从公开数据算出的统计值，论文 Table 2 没有直接给出。

## 4. 指令改写与场景配对

- **10 条指令是同一意图的改写。** 例如 `left_lc` 的 10 条指令：“Make a left lane change.”“Switch to the left lane.”……“Merge left.”。因此“改写一致性”已经部分内置在数据集里。
- **场景种子大多是普通数字，少数很奇怪**（如 `22567687678`、`1847432543253`，主要出现在 `dec_abs_dis20/25`、`right_overtake` 等 JSON 中）。【推断】看起来是手工敲入的数字，没有发现规律，按原样使用即可。
- **不存在“同一场景、不同意图”的配对。** 最接近的是 `left_lc` 和 `right_lc`：两者 `s0`–`s19` 用同一批场景种子（251–270），但自车初始车道总是不同（左变道从 1 号车道出发，右变道从 0 号车道出发）；20 个场景里还有 3 个（`s8`、`s13`、`s18`）的车辆数或密度也不同。所以它们是两个不同的场景。

## 5. Demo 集（12 个样本）

```
dec_abs_dis25_s1_c0     dec_abs_speed10_s0_c0   dec_rel_dis15_s1_c0
dec_rel_speed6_s0_c0    go_straight_s1_c0       left_lc_s0_c0
right_lc_s0_c0          left_overtake_s0_c0     right_overtake_s0_c0
turn_left_s1_c0         turn_right_s1_c0        pull_over_s0_c5
```

- 除 `pull_over_s0_c5` 外都用 `c0` 指令。
- 官方 Few-shot 提示词（`prompts/cg_template_fs.txt`）里有 3 个示例，示例指令分别与 3 个 Demo 样本的指令**逐字相同**：`dec_abs_dis25_s1_c0`（Decrease gap to 25 meters.）、`left_overtake_s0_c0`（Go around the car in front of you using the left lane.）、`go_straight_s1_c0`（Continue straight ahead at the intersection.）。
- Demo 集在 Human Feedback 评测里还有特殊用途，见 [LaMPilot测试划分与论文结果](LaMPilot测试划分与论文结果.md) 第 3 节。

## 6. 评测指标（按代码 `utils/result.py`、`evaluator/base.py`）

| 指标 | 定义 |
| --- | --- |
| 完成率 | 成功样本数 / 全部样本数。代码叫 success rate，论文 Table 3 的“完成率”就是它 |
| 碰撞率 | 发生碰撞的样本数 / 全部样本数 |
| 单样本分数 | 只对成功样本计算，失败记 0；由 TTC、速度方差、时间效率三项加权 |
| Driving Score | 完成率 × 成功样本的平均分数 − 碰撞率 × 500 |

核对：实验 02 的 12 个 Demo 样本全部成功、无碰撞，Driving Score 83.22 正好等于 12 个单样本分数的平均值。

## 7. 本次整理对原文的修正

| 原文写法 | 修正 | 依据 |
| --- | --- | --- |
| “每个 Sample 有一个官方的 seed” | 种子按**场景**给，同一场景的 10 个样本共用 | JSON 中 `seed` 位于 `samples` 元素内 |
| 实验情况说明：“4900 个 ID，而不是 4900 个样本” | 统一为“4,900 个样本，每个样本有一个样本 ID”；与数据集说明里的 Sample = ID 一致 | 术语统一 |
| `dec_abs_dis 25.json` | `dec_abs_dis25.json` | 文件名 |
| “基础场景编号”一列混写数量和编号 | 拆成“场景”（490 个）和“基础场景编号”（`sX`） | 术语统一 |

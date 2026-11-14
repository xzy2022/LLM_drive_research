# LaMPilot 测试划分与论文结果

> 论文：`@2024_CVPR_LaMPilot-Bench`。术语（样本 / 场景 / 任务配置 / 场景种子）见 [LaMPilot数据集结构与术语](LaMPilot数据集结构与术语.md)。
> 来源：合并自 `experiment/exp_1107_@02_lampilot_deepseek_demo/实验情况说明.md`（2026-11-07），并对照本地仓库 `repos/LaMPilot/projects/lampilot/` 的 `test_icl.py`、`test_hf.py`、`test_idm.py`、`dt/hf_agent.py` 复核。

## 1. 论文怎么说，仓库怎么做

论文原文：

> "The LaMPilot dataset consists of 4,900 semi-human-annotated traffic scenes"
> "with a subset of 500 samples split as the test set."

- 论文：4,900 个样本，其中 500 个作为测试集。
- 项目网页：训练 3,900 / 验证 500 / 测试 500（用户记录；本地仓库里没有找到对应的划分文件或 ID 列表）。
- 仓库：没有给出划分方式。`--test-size n` 只是取数据集的前 n 个样本；加 `--shuffle` 时先按 `--random_seed`（默认 42）打乱再取。

各评测脚本的默认值：

| 脚本 | 用途 | `--test-size` 默认值 | 实际评测范围（不打乱） |
| --- | --- | --- | --- |
| `test_icl.py` | Zero-shot / Few-shot | 98 | 前 98 个样本，**全部来自 `dec_abs_dis15` 这一个任务配置**（`s0_c0` 到 `s9_c7`） |
| `test_hf.py` | Human Feedback | 98 | 先跑 12 个 Demo 样本，再跑前 98 个样本，共 110 个（见第 3 节） |
| `test_idm.py` | IDM / MOBIL（不读指令） | 10000 | 全部 4,900 个样本。因为不读指令，同一场景的 10 个样本结果相同，等价于 490 个场景（断点续跑时会按场景跳过已跑过的） |

## 2. 论文 Table 3 的数字反推

| 方法 | 报告值 | 反推 | 说明 |
| --- | --- | --- | --- |
| GPT-4 3-shot 完成率 | 84.7% | 83/98 | 500 作分母得不到 84.7%（423/500 = 84.6%，424/500 = 84.8%） |
| GPT-4 Human Feedback 完成率 | 92.7% | 102/110 | |
| GPT-4 Human Feedback 碰撞率 | 0.9% | 1/110 | |
| IDM 完成率 | 20.4% | 20/98 或 100/490（= 1,000/4,900） | 490 = 5 × 98，几种分母都对得上，无法区分 |
| MOBIL 完成率 | 15.3% | 15/98 或 75/490（= 750/4,900） | 同上 |

结论：【推断】作者声称测试集有 500 个样本，但 Table 3 的 LLM 方法很可能是在仓库默认的 98 个样本上测的，而这 98 个样本只覆盖 `dec_abs_dis15` 一个任务配置。04 阶段对齐论文数字时要注意这一点。

## 3. Human Feedback 的流程和 110 的来源

按 `test_hf.py` 和 `dt/hf_agent.py` 的代码：

1. **先跑 12 个 Demo 样本，有人参与。** 每轮执行完，人在终端输入：是否成功（y/n）、成功时是否存入（commit）、一段文字评语（critique）。
   - 失败：把评语和上一版代码交给 LLM，重新生成策略，**循环直到人判定成功**。
   - 成功且选择存入，且代码超过 2 行：把这段策略代码存进向量库（Chroma + OpenAI embeddings），这就是 HF 的 RAG 库。
2. **再跑前 98 个样本，没有人参与。** 每个样本只生成一次策略；生成前按指令从向量库检索已存的策略（top-k）放进提示词。这一步不再往库里存新策略。
3. **最后把两部分结果合在一起统计。**

所以按默认参数，110 = 12 个 Demo 样本 + 98 个样本。【推断】这比“作者手动设了 `--test-size 110`”更自然。由此还能推出：

- 12 个 Demo 样本在循环里一直重试到人判定成功，必然计为成功。
- 扣除这 12 个后，98 个样本上是 90/98 ≈ 91.8%，与 3-shot 的 83/98 是同一批样本。

原文档写的“用 100 个样本加入反馈做成示例”在代码里找不到依据：RAG 库只来自 12 个 Demo 样本的反馈过程。

## 4. 方法名称对照

| 本项目叫法 | 含义 | 代码 |
| --- | --- | --- |
| Zero-shot | 提示词里没有示例 | `prompts/cg_template_zs.txt` |
| Few-shot / 3-shot | 提示词里有 3 个示例（距离控制、左侧超车、路口直行各一个） | `prompts/cg_template_fs.txt` |
| Human Feedback（HF） | 第 3 节的流程：Demo 样本上人工反馈 + 存入向量库，测试样本上检索 | `test_hf.py`、`prompts/cg_template_hf.txt` |
| IDM / MOBIL | 不读指令的规则控制器基线 | `test_idm.py --method idm / mobil` |

## 5. 本地实验 02 的位置

实验 02 用 `deepseek-flash` + 官方 Few-shot 提示词，跑了 12 个 Demo 样本：12/12 成功，无碰撞，Driving Score 83.22，每样本约 2.8K 输入 + 0.3K 输出 tokens。详见 [实验 02 总结](../../experiment/exp_1107_@02_lampilot_deepseek_demo/summary.md)。

这个结果只说明“API → 代码解析 → 控制器 → 仿真 → 评分”链路已跑通，不能当测试集成绩：

- Demo 集不是论文的 500 个测试样本，也不是仓库默认的 98 个样本。
- 其中 3 个 Demo 样本的指令与 Few-shot 示例逐字相同。

## 6. 本次整理对原文的修正

| 原文写法 | 修正 | 依据 |
| --- | --- | --- |
| “没有指定 `--test-size` 时默认是 83，83 作为分母…” | 默认值是 **98**；98 是分母，83 是分子（83/98 = 84.7%） | `test_icl.py` 第 30 行 |
| “HF 评估时使用了 `--test-size 110`” | 更可能是 12 个 Demo 样本 + 默认 98 个样本 = 110 | `test_hf.py` 的执行顺序 |
| “HF：用 100 个样本加入反馈做成示例并构建 RAG 库” | RAG 库来自 12 个 Demo 样本上的人工反馈；98 个测试样本只检索、不反馈 | `test_hf.py`、`dt/hf_agent.py` |
| 未提 IDM / MOBIL 的分母 | 它们的脚本默认跑全部 4,900 个样本（等价于 490 个场景），数字也能被 98 解释，无法区分 | `test_idm.py` |

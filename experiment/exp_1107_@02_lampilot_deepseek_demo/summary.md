# 实验 02：DeepSeek 真实 API 小规模验证

- 项目：`@2024_CVPR_LaMPilot-Bench`。
- 状态：历史实验已完成，本次仅事后整理；流程缺口见 [笔记](notes.md) 和 [时间](time.md)。
- 仓库：`../../repos/LaMPilot`。初始化 `9e6de81`，适配 `a520dd4`，共用入口 `f9fb829`，原结果说明 `54d8a52`。
- 真实运行时 Git HEAD：`1af618799c35969d3db61578dd66daed43439536`。原代码 / 提示词哈希见 [manifest](logs/runs/deepseek-demo12/manifest.json)，未改写。
- 环境：Windows 11，Conda `lampilot_py311`，Python 3.11.18，RTX 5060 Laptop 约 8GB；沿用 [实验 01](../exp_1107_@01_lampilot_environment/summary.md) 的环境。
- 入口：子仓库 `reproduction/run.ps1` / `reproduction/run_small.py`，原命令见 [笔记](notes.md)。
- 模型：`deepseek-flash`，原版 Few-shot，temperature=0，thinking disabled，输出上限 2,048 tokens。

## 原有结果

| 指标 | 固定 12 个 Demo 批次 |
| --- | ---: |
| 完成仿真 | 12/12 |
| 官方评分器判定成功 | 12/12 |
| 碰撞 | 0 |
| API / 入口异常 | 0 |
| 日志中的策略执行异常 | 0 |
| Driving Score | 83.221336 |
| 输入 tokens | 33,210 |
| 输出 tokens | 3,416 |
| 总 tokens | 36,626 |
| 输入缓存命中 / 未命中 tokens | 29,312 / 3,898 |

正式批次前有一个首样本预检，成功且无碰撞，返回 3,104 tokens。因此共有 13 份成功响应、12 个唯一样本，合计 39,730 tokens；没有增加随机种子。本次整理没有生成新的 API 响应。

## 逐场景原结果

| ID | 原场景种子 | 成功 | 碰撞 | 分数 | 仿真秒 | tokens |
| --- | ---: | --- | --- | ---: | ---: | ---: |
| `dec_abs_dis25_s1_c0` | 22567687678 | 是 | 否 | 89.114 | 11.5 | 3,093 |
| `dec_abs_speed10_s0_c0` | 41 | 是 | 否 | 68.363 | 9.2 | 2,819 |
| `dec_rel_dis15_s1_c0` | 82 | 是 | 否 | 92.858 | 5.2 | 3,122 |
| `dec_rel_speed6_s0_c0` | 111 | 是 | 否 | 93.377 | 6.2 | 2,925 |
| `go_straight_s1_c0` | 432 | 是 | 否 | 78.218 | 15.5 | 3,108 |
| `left_lc_s0_c0` | 251 | 是 | 否 | 99.297 | 0.9 | 2,936 |
| `left_overtake_s0_c0` | 271 | 是 | 否 | 84.583 | 11.3 | 3,109 |
| `pull_over_s0_c5` | 311 | 是 | 否 | 71.090 | 6.2 | 3,062 |
| `right_lc_s0_c0` | 251 | 是 | 否 | 99.141 | 0.9 | 2,944 |
| `right_overtake_s0_c0` | 1847432543253 | 是 | 否 | 57.183 | 8.1 | 3,145 |
| `turn_left_s1_c0` | 332 | 是 | 否 | 84.171 | 16.5 | 3,206 |
| `turn_right_s1_c0` | 382 | 是 | 否 | 81.262 | 15.2 | 3,157 |

## 证据

- [正式批次汇总](logs/runs/deepseek-demo12/summary.json)、[逐场景结果](logs/runs/deepseek-demo12/results.json)、[配置和哈希](logs/runs/deepseek-demo12/manifest.json)。
- [单样本预检汇总](logs/runs/deepseek-one/summary.json)。
- 逐场景文件夹保留 `prompt.json`、`response.json`、`policy.json`、`result.json`、`run.log`、初始 / 最终 PNG。
- 右转图像：[初始](figures/turn_right_initial.png) / [最终](figures/turn_right_final.png)。原始图像也保留在对应运行目录中。
- [原结果文档](logs/legacy_documents/deepseek_results.md) 原样保留；该旧文档中的旧路径不作为现行导航。

## 结论与边界

历史结果表明真实 API → 代码解析 → 控制器 → 仿真 → 评分和保存的链路已跑通。12 个 Demo 与部分官方 Few-shot 示例任务对应，不能将 12/12 成功解释为独立测试集 100% 或泛化 / 普遍安全性。本轮没有模型对比、Human Feedback 或多随机种子结果。

本次只搬迁和读取已有证据，没有重跑实验。旧实验分支、squash 和三个规定时间缺失，均保留为历史特殊情况；详见 [提交对照](../commit_history.md)。

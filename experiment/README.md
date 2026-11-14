# 实验索引

实验流程以 [实验通用原则](../ai_read/实验通用原则.md) 为准。项目代码位于 `repos/` 独立仓库；实验文档、日志和图像集中在本目录。

| 编号 / 目录 | 内容 | 状态 | 入口 |
| --- | --- | --- | --- |
| `exp_1107_@01_lampilot_environment` | LaMPilot 的 Windows 环境配置及离线检查 | 历史实验已完成；流程记录缺口列为特殊情况 | [总结](exp_1107_@01_lampilot_environment/summary.md) · [笔记](exp_1107_@01_lampilot_environment/notes.md) · [时间](exp_1107_@01_lampilot_environment/time.md) |
| `exp_1107_@02_lampilot_deepseek_demo` | DeepSeek 真实 API 预检及固定 12 个 Demo | 历史实验已完成；流程记录缺口列为特殊情况 | [总结](exp_1107_@02_lampilot_deepseek_demo/summary.md) · [笔记](exp_1107_@02_lampilot_deepseek_demo/notes.md) · [时间](exp_1107_@02_lampilot_deepseek_demo/time.md) |

这两个目录是按新规范追溯整理已有实验，不是本次重新执行的实验。离线调试、超时检查和模拟 API 错误都归入环境配置实验，不另增实验编号；单样本 API 预检归入 DeepSeek 实验。

旧实验未创建同名分支、未按实验 squash、未记录三个要求的时间，均如实标注为历史特殊情况。保留原提交哈希，不伪造分支或时间，不重写 Git 历史。

- [提交与文档迁移对照](commit_history.md)：既有提交归属、新旧位置和缺口。
- [迁移校验清单](migration_20261107.json)：308 个原有文件的来源、目标、字节数和 SHA-256。
- `logs/legacy_documents/` 保存原始旧文档，仅作为历史证据；旧链接和命令未改写，当前导航以各实验的 `summary.md` / `notes.md` 为准。

本次只调整架构、文档位置和运行入口的输出路径约束，没有调用 API、启动仿真、重装环境或补跑测试。父项目的改动留给用户决定暂存和提交。

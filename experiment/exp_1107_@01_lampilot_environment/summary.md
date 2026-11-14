# 实验 01：LaMPilot 环境配置与离线检查

- 项目：`@2024_CVPR_LaMPilot-Bench`。
- 状态：历史实验已完成，本次仅事后整理；缺失流程见 [笔记](notes.md) 和 [时间记录](time.md)。
- 代码仓库：`../../repos/LaMPilot`，保持独立 Git 历史。
- 初始化：`9e6de81`；环境提交：`c7340dd`；共用入口：`f9fb829`；原环境说明：`1af6187`。
- 最终离线运行记录的 Git HEAD：`f9fb829f8407dcdd4fd1a3c00acdc2e91b1bc458`。运行时代码哈希保留在原 manifest 中，本次不更新为整理后的版本。

## 环境和启动入口

历史运行环境为 Windows 11、RTX 5060 Laptop 约 8GB 显存，Conda `lampilot_py311`，Python 3.11.18。场景仿真和云端 API 路线不依赖本地 CUDA 推理。环境文件逻辑大小当时约 602MiB，不含下载缓存。

安装依赖、锁定文件和入口继续保留在子仓库 `reproduction/`，来源记录迁至 [source.json](logs/source/source.json)。上游提交为 `ba4564e28a32935f2a5de7b1b85bed7289fcebdb`。

当时运行入口为 `reproduction/run.ps1 -Mode offline`，原默认输出是子仓库 `ckpt/offline-validated`。此处只记录历史命令，不在本次执行；新入口已取消仓库内默认输出，未来运行必须显式传入新实验的外部输出目录。

## 已有结果

| 检查 | 历史结果 |
| --- | --- |
| 依赖检查 | 当时 `pip check` 通过，本次未重新执行 |
| 官方全量 / Demo 加载 | 4,900 / 12 个样本 |
| 最终 12 个 Demo 离线仿真 | 12/12 完成，入口异常 0 |
| 人工设速策略 | 目标 10m/s；官方评分器判定成功，无碰撞；仿真 9.2 秒，分数 68.362610 |
| 离屏截图 | 初始、最终 PNG 正常；早期黑图诊断单独保留 |
| 超时 / 跳过已有结果 / 模拟 API 错误 | 原记录已保留；这些是环境检查，不计为真实 API 实验 |

离线策略由一个人工设速策略与其余 autopilot 检查组成，原汇总为成功 3/12、碰撞 1/12。其用途是验证代码执行、仿真和评分链路，不能作为 DeepSeek 性能。

## 证据

- [最终汇总](logs/runs/offline-validated/summary.json)、[结果](logs/runs/offline-validated/results.json)、[原配置和哈希](logs/runs/offline-validated/manifest.json)。
- [人工设速结果](logs/runs/offline-validated/dec_abs_speed10_s0_c0/result.json)。
- 图像：[初始](figures/offline_speed_initial.png) / [最终](figures/offline_speed_final.png)。
- 原始混合说明：[验证记录](logs/legacy_documents/validation.md)、[原运行说明](logs/legacy_documents/reproduction_README.md)，只作历史证据。

结论：该环境已具备运行小规模 LaMPilot 场景的条件。此结论来自已完成的历史检查；本次没有安装、运行或重新验证实验能力。

# LaMPilot 历史提交与文档整理对照

本次整理保留子仓库原有六个提交及哈希。两次历史实验的实现存在交叉，不能事后冒充两个独立、连续的实验分支；缺失的标准流程列为特殊情况。

## 子仓库既有提交

仓库：`repos/LaMPilot`，分支 `main`。

| 提交 | 原提交说明 | 归属 / 用途 |
| --- | --- | --- |
| `9e6de81` | 初始化：导入 LaMPilot 官方原始源码 | 两个实验共同使用的初始化基线 |
| `c7340dd` | 环境：固定 Windows 复现依赖并记录官方源码版本 | 实验 01：依赖、来源及环境约定 |
| `a520dd4` | 适配：接入 DeepSeek 并记录模型输出和用量 | 实验 02：DeepSeek 适配实现；离线契约检查归入实验 01 |
| `f9fb829` | 运行：增加固定样本评测与离屏渲染及超时恢复入口 | 两个实验共用的运行入口；离线最终记录的运行版本 |
| `1af6187` | 文档：记录 Windows 离线验证结果与 DeepSeek 运行方法 | 实验 01 的旧说明；实验 02 真实运行时的 Git HEAD |
| `54d8a52` | 实验：记录 DeepSeek 十二个场景真实运行结果 | 实验 02 的原结果说明；整理前子仓库 HEAD |

历史实验未建立同名分支，未在正式运行前进行 squash。没有补建假的历史实验分支，也没有将上述提交重写为两个看似按新流程执行的提交。

本次维护性整理的子仓库提交会移除已迁出的本地实验文档和来源记录，更新必要操作约定，并要求运行入口显式把输出写到父项目 `experiment/`。此维护提交不算第三个实验，也不是前两次实验的追溯 squash。维护提交哈希在本页末尾记录。

## 父项目历史提交

| 提交 | 内容 | 本次处理 |
| --- | --- | --- |
| `9f849c6` | 隔离子仓库、增加 `repos/README.md` | 保留，属于新实验规范建立前的历史操作 |
| `4c644f6` | 增加旧实验文档导航 | 保留历史；当前工作区导航改指 `experiment/` |

当前父项目已有用户暂存的修改；本次不执行父项目 `git add` 或 `git commit`，不改变原暂存内容。

## 文档与产物迁移

| 原位置 | 新位置 |
| --- | --- |
| `repos/LaMPilot/reproduction/README.md` | 实验 01 的 `logs/legacy_documents/reproduction_README.md`，有效内容拆入两次实验的笔记 |
| `repos/LaMPilot/reproduction/validation.md` | 实验 01 的 `logs/legacy_documents/validation.md`，有效内容拆入两次实验总结 |
| `repos/LaMPilot/reproduction/deepseek_results.md` | 实验 02 的 `logs/legacy_documents/deepseek_results.md`，当前结果入口为该实验 `summary.md` |
| `repos/LaMPilot/reproduction/source.json` | 实验 01 的 `logs/source/source.json` |
| `repos/LaMPilot/ckpt/offline-*`、`ckpt/_contract_checks` | 实验 01 的 `logs/runs/`，保持每次运行的内部文件结构 |
| `repos/LaMPilot/ckpt/deepseek-one`、`ckpt/deepseek-demo12` | 实验 02 的 `logs/runs/`，保持每次运行的内部文件结构 |
| 代表性 PNG | 各实验 `figures/` 保存副本；原图仍在对应运行记录中 |

`reproduction/` 只保留 Python/PowerShell 入口和依赖清单；原项目自带的 README、提示词说明等上游文件保持原样。API Key 仍在子仓库被忽略的 `.env`，没有迁入实验归档。

## 特殊情况

1. 两个历史实验的三个规定时间都缺少原始专用记录，在各自 `time.md` 标为缺失；Git 提交时间仅作旁证。
2. 缺少同名实验分支和 squash 提交，按历史例外保留，不伪造合规历史。
3. Git 模块提交、离线检查和正式运行当时的顺序不完全符合新流程；当前可用证据不能证明所有正式运行都严格对应当时的干净 Git 提交。
4. 原始源码 ZIP `tmp/lampilot-upstream.zip` 当前缺失；原 `source.json` 中的 SHA-256 和初始化 Git 源码仍保留，不补下载。
5. 旧调试目录有失败、超时和模拟错误记录，这是环境检查的真实历史，不补做、不删除，也不计为真实 DeepSeek 调用。
6. 论文独立 500 样本、全量 4,900 样本、Human Feedback 和多随机种子实验均未开展，属于范围外未执行项，不补造结果。

## 本次整理校验

校验范围仅为文件 SHA-256、归档内容完整性、活动文档链接、Python / PowerShell 语法、官方代码差异和 Git 状态。不运行任何实验入口，不产生新的模型或仿真结果。

- 子仓库维护提交：`9728f21`，`整理：迁出历史实验记录并统一外部输出目录`。
- 原有 308 个文件、806,687 字节全部按清单迁移，SHA-256 一致；4 张代表图像副本与原图一致。
- 12 份活动文档链接校验通过；历史原文档中的旧链接不作活动导航。
- Python AST 和 PowerShell 解析检查通过，均未执行运行入口；本次新 API 调用和新仿真次数均为 0。
- 官方 `highway_env/` 与 `projects/` 相对初始化提交无变化。
- 父项目 HEAD 和原暂存内容保持不变。本次新增实验归档与导航修改均未由助手暂存或提交。

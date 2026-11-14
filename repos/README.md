# 独立复现仓库

`repos/` 下每个项目使用自己的 `.git`，由主仓库的 `.gitignore` 排除工作区内容。
这是独立嵌套仓库，不是 Git submodule；主仓库不会记录子仓库内部代码变化。

规则：

1. 导入上游项目后，先提交一次未经功能修改的初始化版本，并记录来源版本。
2. 新实验遵循 [实验通用原则](../ai_read/实验通用原则.md)：先建父项目实验目录与时间记录，再建同名实验分支，持续中文提交，小样本检查后按规范 squash 到主分支。
3. 提交前确认 `git rev-parse --show-toplevel` 指向预期仓库。
4. API Key 不进入 Git；依赖声明留在代码仓库，实验说明、日志和图像放在父项目 `experiment/`。分析后不自动暂存或提交父项目。

## LaMPilot

- 路径：`repos/LaMPilot`
- 上游：<https://github.com/PurdueDigitalTwin/LaMPilot>
- 导入的上游提交：`ba4564e28a32935f2a5de7b1b85bed7289fcebdb`（`master`）
- 本地初始化提交：`9e6de81`，`初始化：导入 LaMPilot 官方原始源码`
- 上游源码通过本机 GitHub CLI 下载官方归档；本地 Git 历史从初始化提交开始。
- 实验 01：[环境配置与离线检查](../experiment/exp_1107_@01_lampilot_environment/summary.md)。
- 实验 02：[DeepSeek 真实 API 小规模验证](../experiment/exp_1107_@02_lampilot_deepseek_demo/summary.md)。
- 历史提交、文档位置及特殊情况：[整理对照](../experiment/commit_history.md)。
- 子仓库 `reproduction/` 仅保留入口和依赖声明，输出必须显式指定到父项目 `experiment/` 下；旧实验记录已经迁出。

检查子仓库：

```powershell
git -C repos/LaMPilot status
git -C repos/LaMPilot log --oneline -5
```

## DiLu

- 论文：`@2024_ICLR_DiLu`。
- 路径：`repos/DiLu`；上游：<https://github.com/PJLab-ADG/DiLu>。
- 导入版本：`main` 的 `74c4aa96a8f5816731d5eb5cc1d93add30674287`；通过本机 GitHub CLI 下载该提交的官方归档，子仓库保留独立本地历史。
- 本地初始化提交：`fb6e5fc`；包含上游配置、示意图和原始记忆库文件。
- DeepSeek 准备记录与使用命令：[实验说明](../experiment/exp_1113_@01_dilu_deepseek_prepare/notes.md)、[总结](../experiment/exp_1113_@01_dilu_deepseek_prepare/summary.md)。默认零样本小规模配置；完整记忆检索尚需单独验证。

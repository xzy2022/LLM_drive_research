# 实验 02 笔记与历史特殊情况

## 实验设计

在实验 01 的 Windows / Conda 环境上，使用 DeepSeek API 生成策略，本地执行官方 LaMPilot 控制器、仿真和评分器。先验证一个场景，再运行官方 `DbLv1DemoDataset` 的固定 12 个场景，保留原种子，不做额外随机种子重复。

模型为 `deepseek-flash`，Few-shot，temperature=0，thinking disabled，输出上限 2,048 tokens。API 单次超时 90 秒、最多额外重试一次，单个工作进程上限 240 秒。

DeepSeek 适配使用原版提示词、消息构造和代码解析器，增加了用量记录、截断输出拒绝和空策略拒绝，没有修改官方仿真、控制或评分算法。

## 历史启动记录

当时从子仓库执行：

```powershell
.\reproduction\run.ps1 -Mode api -Limit 1 -Output ckpt/deepseek-one
.\reproduction\run.ps1 -Mode api -Output ckpt/deepseek-demo12
```

以上是历史命令，本次不执行，也不作为当前复用指令。运行记录已迁至本实验 `logs/runs/`；当前入口要求输出位于父项目 `experiment/`，不再支持向子仓库 `ckpt/` 写入。

API Key 仍在 `repos/LaMPilot/.env`，没有迁入文档或归档。当前支持进程环境变量和指定 `.env`；不要在终端输出或 Git 中记录密钥。

## 结果适用范围

这 12 个 Demo 用于确认真实 API 到评分的完整链路。官方 Few-shot 示例包含跟车间距、左侧超车、交叉口直行等任务，与部分 Demo 对应；12/12 成功不能视为独立测试集成绩。

预检和正式批次重复了同一个首样本，共 13 份成功响应、12 个唯一样本，不是多随机种子实验。用户报告当时账单约两分钱；这是用户观察值，日志只保存返回 token 用量，未保存账单证据。

## 历史特殊情况

1. 当时没有预建实验目录或三个专用时间记录，见 `time.md`。
2. 未创建与实验编号相同的历史分支，未按“分支小样本 → squash → 正式运行”流程执行，原提交与运行记录如实保留。
3. 原始结果里的 Git HEAD `1af6187` 与代码哈希代表运行时状态；整理后入口代码改变，不改写原 manifest，也不以新代码重跑以制造一致记录。
4. 子仓库当时只保存了逐场景日志，没有单独持久化完整批处理控制台输出。本次不补造这份日志。
5. 论文独立 500 样本、全量 4,900 样本、Human Feedback 和更多种子均未执行，属于范围外未开展项，没有结果。

## 本次整理边界

本次没有发送 DeepSeek 请求或运行任何仿真。已有响应、提示词、策略、评分、图像和日志逐文件迁移并做 SHA-256 校验。旧结果说明原样保存在 `logs/legacy_documents/deepseek_results.md`；有效导航和汇总以本实验 `summary.md` 为准。

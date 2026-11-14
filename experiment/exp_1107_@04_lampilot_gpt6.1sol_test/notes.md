# 实验 04 笔记与踩坑记录

## 1. 实验思路与设计决策

1. **隐私与安全保护**：
   - 严格遵照用户指令：不阅读、不输出、不归档 `repos/LaMPilot/.env` 文件本身。
   - 适配 `load_key` 机制，使其仅在进程内存中读取 `GPT_API_KEY`，日志输出中自动替换所有可能的敏感 token。
2. **推理模型接入机制（GPT-6.1 Sol）**：
   - 模型在 OpenAI 体系下为推理模型（Reasoning Model），支持设置 `reasoning_effort="low"`（低级思考模式）。
   - **踩坑记录**：OpenAI 对推理模型的 Chat Completions API 实施严格校验——当启用了思考模式时，请求体内**禁止传递 `temperature` 参数**，否则直接报 HTTP 400 校验错误。为此构建了 `ReasoningChatOpenAI` 子类，在发送 payload 前剔除 `temperature` 字段，确保接口顺利调用。

---

## 2. 仿真行为与评测器对齐分析

1. **聪明反被聪明误（Early Return 陷阱）**：
   - GPT-6.1 Sol 相比 DeepSeek 显示出更强的代码自主构造能力（增加了 `headway >= 0.6` 保护与步长平滑化）。
   - 但它“自作主张”地添加了：
     ```python
     if 14.0 <= gap <= 16.0:
         say('The following gap is approximately 15 meters.')
         return
     ```
   - 在 LaMPilot 的官方评测器设计中，评测器是黑盒运行的，要求自车**持续保持在区间内连续 5 秒**。模型策略一旦 `return`，生成器即告终止，后续便不再根据动态车距微调时距，导致因微小速度差漂出区间并最终判定超时失败。
2. **明天全量测试的对比意义**：
   - 如果保持原版 3-shot 提示词不变跑全量 98 个样本，我们可以真实观测到 GPT-6.1 Sol 在不同指令下的表达风格和自主推断逻辑。
   - 额度方面：98 个样本总消耗预估仅约 **0.4 美元（约 2.9 元人民币）**，完全在可承受的安全预算范围内。

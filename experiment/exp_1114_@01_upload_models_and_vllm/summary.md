# 本地模型上传与 vLLM 加载验证结果报告

- **实验项目**：服务器模型部署与 vLLM 加载验证
- **父仓库 Git 提交哈希**：`693e4ac3dce34221ff261232d4729ee6a0048785`（根据规范，分析完成后不自动执行父项目提交，等待人工决定）
- **服务器环境**：
  - 宿主机系统：Ubuntu 22.04.5 LTS (x86_64)
  - 显卡配置：8×NVIDIA GeForce RTX 4090 (24GB VRAM)，驱动版本 595.99.02
  - 测试显卡：GPU 0（单卡运行，其余 7 卡空闲）
  - Conda 环境：`/data/xxx/conda/envs/vllm` (Python 3.12.16, PyTorch 2.14.0+cu130, vLLM 0.33.0)
  - 远程模型存放根目录：`/data/xxx/models/`

---

## 一、 模型上传结果清单与完整性校验

从本地 `E:\models\` 传输至服务器 `/data/xxx/models/`，全量 6 个模型传输完成，文件数量与体积均 100% 对齐校验通过：

| 模型名称 | 本地文件数 | 远程文件数 | 服务器磁盘占用 | 传输耗时 | 校验状态 |
|---|---|---|---|---|---|
| `DeepSeek-R1-Distill-Qwen-1.5B` | 10 | 10 | 3.4 GB | ~30 秒 | ✅ 完全一致 |
| `DeepSeek-R1-Distill-Qwen-7B` | 12 | 12 | 15 GB | 2分11秒 | ✅ 完全一致 |
| `Qwen2.5-Coder-7B-Instruct` | 15 | 15 | 15 GB | 2分10秒 | ✅ 完全一致 |
| `Qwen3.5-4B` | 15 | 15 | 8.8 GB | 1分20秒 | ✅ 完全一致 |
| `Qwen3.5-9B` | 17 | 17 | 19 GB | 2分46秒 | ✅ 完全一致 |
| `Qwen2.5-Coder-14B-Instruct` | 17 | 17 | 28 GB | 4分14秒 | ✅ 完全一致 |
| **总计** | **86** | **86** | **约 89.2 GB** | **约 13 分钟** | **全部就绪** |

---

## 二、 vLLM 模型加载与推理测试结果

- **测试脚本**：`test_vllm_load.py`
- **执行方式**：单卡 `CUDA_VISIBLE_DEVICES=0`
- **目标模型**：`/data/xxx/models/DeepSeek-R1-Distill-Qwen-1.5B`
- **模型架构识别**：`Qwen2ForCausalLM`
- **推理精度**：`torch.bfloat16`
- **Attention 后端**：`FLASH_ATTN` (FlashAttention v2)
- **Top-p/Top-k 采样后端**：`FlashInfer`

### 1. 启动与显存数据
- 模型权重占用：**3.45 GiB**，加载耗时 0.67 秒。
- KV Cache 分配：**9.54 GiB**（支持最大 357,264 tokens 缓存）。
- CUDA Graph 捕获耗时：3 秒。
- 引擎端到端预热总耗时：82.8 秒。

### 2. 文本生成与吞吐指标
- 实测生成输出吞吐：**565.74 tokens/s**。
- 输出测试样例：
  - Prompt: `"Please provide a one-sentence summary of autonomous driving."`
  - Response: `"Autonomous driving is a technology that allows vehicles to operate independently without human intervention, using algorithms and systems to control and make decisions based on real-time data."`
- 退出行为：测试结束后自动触发 `EngineCore` 优雅停机并释放全部显存，`nvidia-smi` 验证 GPU 显存完全恢复至 18 MiB 待机状态。

---

## 三、 单卡运行模型选型建议

在单张 RTX 4090 (24GB 显存) 环境下：
1. **单卡主力推荐（速度与智力黄金平衡点）**：
   - **7B ~ 9B 模型**（如 `Qwen2.5-Coder-7B-Instruct`、`DeepSeek-R1-Distill-Qwen-7B`、`Qwen3.5-9B`）。
   - 权重占 14~18 GB，剩余 6~10 GB 显存足以作为 KV Cache 承载 4K~8K 长文本对话，原生 BF16 无损运行，单卡吞吐可达 50~80 tokens/s。
2. **轻量与低延迟推荐**：
   - **1.5B ~ 4B 模型**（如 `DeepSeek-R1-Distill-Qwen-1.5B`、`Qwen3.5-4B`）。
   - 启动极快，显存占用极小，吞吐 >150~500 tokens/s，适合大规模高并发调用或快速原型实验。
3. **14B 模型运行建议**：
   - `Qwen2.5-Coder-14B-Instruct` 权重需 28 GB，单卡原生 BF16 无法完整装载。
   - 推荐方案：服务器拥有 8 张 4090，建议直接使用 **双卡张量并行**（`tensor_parallel_size=2`，例如使用 GPU 0,1），免量化、无精度损失且速度极佳。

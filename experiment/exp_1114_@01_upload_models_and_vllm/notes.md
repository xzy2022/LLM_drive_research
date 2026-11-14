# 实验笔记与经验总结

## 一、 实验思路与执行流程

1. **环境与网络探测**：
   - 先通过 `Get-NetAdapter` 和 `Get-NetIPAddress` 确认物理连接走的是千兆有线网卡（1 Gbps）而非无线 Wi-Fi，从而能准确计算 86GB 数据传输时长（约 13~15 分钟）。
   - 远程创建模型存放目录 `/data/xxx/models/`，确认磁盘剩余 547 GB，空间完全充裕。

2. **分阶段与并发执行**：
   - 策略：先上传轻量模型 `DeepSeek-R1-Distill-Qwen-1.5B`（3.4 GB，约 30 秒），立即验证 vLLM 链路闭环。
   - 在验证 vLLM 的同时，启动后台脚本顺序传输其余 5 个大模型，最大化重叠计算与 IO 时间。

## 二、 踩坑记录与关键排查

### 坑 1：FlashInfer JIT 编译寻找 CUDA Toolkit 链接库失败
- **现象**：
  vLLM 首次跑模型时，FlashInfer 自动尝试为 Ada 架构（sm_89）JIT 编译 sampling 算子，报出 `/usr/bin/ld: cannot find -lcudart: No such file or directory`。
- **根本原因**：
  在 pip 规范的 NVIDIA CUDA 独立分发包中（位于个人 Conda 环境内 `/data/xxx/conda/envs/vllm/lib/python3.12/site-packages/nvidia/cu13`），库目录名称为 `lib` 而非传统 Linux 的 `lib64`，且只包含了带版本号的文件名 `libcudart.so.13`，未生成不带版本号的 `libcudart.so` 软链接。当 FlashInfer 编译参数传入 `-L$CUDA_HOME/lib64 -lcudart` 时发生查找失败。
- **解决方案**：
  在个人私有目录 `$CUDA_HOME`（`/data/xxx/conda/envs/vllm/lib/python3.12/site-packages/nvidia/cu13/`）中：
  - 创建软链接 `lib64 -> lib`；
  - 在 `lib/` 下创建软链接 `libcudart.so -> libcudart.so.13` 及相关主要算子库软链接；
  - 并在 `stubs/` 下链接系统现有驱动 `libcuda.so`。
- **安全性与隔离保证**：
  所有软链接严格在用户私有 Conda 目录内，未修改任何 `/usr`、`/etc` 或宿主机驱动，0 权限提升（无 sudo），对服务器其他用户 0 影响。

### 坑 2：PowerShell 中执行多层引号与环境变量转义
- 在本地 PowerShell 调用远程 bash 命令时，由于 `$` 符号会被本地 PowerShell 解析，导致远程变量为空。
- 解决：将复杂执行脚本写为独立 `.sh` 文件并传输至服务器执行，避免 shell 转义混淆。

## 三、 潜在担忧与后续建议

1. **多用户显卡冲突防范**：
   服务器共 8 张 RTX 4090，每次启动推理服务或实验前，必须通过 `nvidia-smi` 检查可用显卡索引，显式使用 `CUDA_VISIBLE_DEVICES=<ID>` 绑定，禁止占用他人正在计算的卡。
2. **14B 模型启动方式**：
   `Qwen2.5-Coder-14B-Instruct` 在 24GB 单卡下会爆显存。后续若需运行该模型，请务必设置 `tensor_parallel_size=2` 并指定两张空闲卡（例如 `CUDA_VISIBLE_DEVICES=0,1`）。
3. **vLLM 内存利用率设置**：
   默认 `gpu_memory_utilization=0.9` 会把整张卡大部分显存作为 KV Cache 锁死。单卡测试时可按需设为 `0.6` ~ `0.8`，避免过度占用显卡资源。

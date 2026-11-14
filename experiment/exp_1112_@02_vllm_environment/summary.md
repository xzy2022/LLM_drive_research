# vLLM 独立环境安装结果

状态：2026-11-12 22:22:17 完成安装及核心验证，之后普通 SSH 环境激活和 `vllm --version` 检查也通过。使用既有 [Wi-Fi 下载脚本](../../ai_read/scripts/Connect-ServerWifi.ps1)，所有下载发生在服务器，出口为电脑 WLAN。没有下载模型、启动推理服务或修改系统驱动。

## 当前组合

| 项目 | 实测值 |
| --- | --- |
| 系统 | Ubuntu 22.04.5、x86_64、glibc 2.35 |
| GPU | 8×RTX 4090，算力 8.9，每卡 24,564 MiB |
| NVIDIA 驱动 | 595.99.02 |
| nvidia-smi CUDA 显示 | 13.2，表示驱动支持版本 |
| Python | 3.12.16 |
| vLLM | 0.33.0 |
| PyTorch | 2.14.0+cu130 |
| PyTorch CUDA 运行时 | 13.0 |
| CUDA Toolkit 组件集 | cuda-toolkit 13.0.3.0 |
| nvcc / nvrtc / nvvm / nvjitlink | 13.0.88 |
| 环境目录 | `/data/xxx/conda/envs/vllm` |
| 环境磁盘占用 | 约 9.6 GiB，不含模型 |
| 保留缓存 | pip 约 4.6 GiB、Conda 约 121 MiB |

固定 vLLM 0.33.0 是依据 [PyPI 版本元数据](https://pypi.org/pypi/vllm/0.33.0/json)，其要求 torch 2.14.0；该 [PyTorch 元数据](https://pypi.org/pypi/torch/2.14.0/json) 要求 CUDA Toolkit 13.0.3 组件。Python 3.12 属于官方支持范围。驱动满足 [NVIDIA CUDA 13.x 最低要求](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html)，并以实际 GPU 检查确认本次基础用途可用。

## 使用

```bash
conda activate /data/xxx/conda/envs/vllm
python -V
vllm --version
```

普通 `ssh xxx` 连接即可激活；后续需要电脑 Wi-Fi 下载时再打开临时代理终端。环境激活变量保存在本环境 Conda 状态中：`CUDA_HOME=/data/xxx/conda/envs/vllm/lib/python3.12/site-packages/nvidia/cu13`，`TRITON_CACHE_DIR=/data/xxx/cache/triton`。没有设置全局 CUDA_HOME、LD_LIBRARY_PATH 或永久代理。

## 验证与证据

- `pip check`：No broken requirements found。
- 读取 8 张卡的设备属性，均为 RTX 4090、算力 8.9。
- GPU 0 小矩阵乘法与 CPU 结果一致。
- 当前平台加载 `_C_stable_libtorch`，实际执行 `torch.ops._C.silu_and_mul`，与 PyTorch 参考实现一致。
- 实际编译并执行小型 Triton kernel，输出与参考结果一致。
- 普通 SSH 激活后，Python、ninja、CUDA_HOME、nvcc 版本和 `vllm --version` 正常。
- 下载会话结束后服务器默认路由仍为 `10.42.0.1/ens111f0`，普通 SSH 没有 HTTP/HTTPS/ALL_PROXY，18797 无残留转发监听。
- 从清华下载的 336,361,138 字节 vLLM wheel，与官方 PyPI SHA-256 一致：`4b6bdec4ab269990bf70d45a3c1e94c3760a27064513760193b26d6f0da883aa`。

本地机器可读结果：[verification.json](verification.json)、[wheel-integrity.json](wheel-integrity.json)、[selection.json](selection.json)。环境锁定记录：[requirements-freeze.txt](requirements-freeze.txt)、[conda-explicit.txt](conda-explicit.txt)。安装输入：[install.sh](install.sh)、[cuda-constraints.txt](cuda-constraints.txt)、[verify.py](verify.py)。服务器原始记录位于 `/data/xxx/setup_records/exp_1112_02_vllm_environment`，本地执行日志位于本实验 `logs/`。

## 源与网络

服务器原来已有国内镜像映射，包括 defaults/conda-forge/pytorch→清华、nvidia→南科大。本次 Conda 以完整官方 conda-forge URL 创建 Python；pip 官方包站实测仅约 22 KB/s 后临时改用清华源，同文件 1 MiB 测试约 1 MB/s。没有修改持久源配置。

当前 Wi-Fi DIRECT 路径可访问 Conda/PyPI；本次 Hugging Face 和 Google 测试 TLS 超时。创建环境不等于后续模型站点已经可达，也没有提供代理节点转发。

## 过程限制

首次安装的依赖解析默认引入了 CUDA 13.5 编译工具，已根据 13.0.3 元数据通过约束统一到 13.0，防止新 PTX 与现有驱动不兼容。旧验证脚本的扩展名、SiLU Python 包装入口已按 0.33.0 的实际接口修正，详细记录见 [notes.md](notes.md)。

本次未测试模型加载、文本生成、FlashInfer 所有后端或多卡张量并行；不能把基础安装通过等同于特定模型端到端验证通过。父项目没有执行 Git 提交，整理时 HEAD 为 `bd2133be2228bac5a13604f7f1dac07a6fe93c20`，安装文件仍以当前工作区和导出的依赖清单为准；无对应 repos/ 子项目，所以没有子项目实验分支。

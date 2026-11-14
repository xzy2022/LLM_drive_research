# 选择与范围

- 目标：用户授权创建独立 Conda 环境并安装适配当前服务器的 vLLM，使用既有 Wi-Fi / SSH 临时代理下载。
- 当前服务器：Ubuntu 22.04.5、x86_64、glibc 2.35、8×RTX 4090 24 GB、NVIDIA 驱动 595.99.02。`nvidia-smi` 报 CUDA 13.2；PATH 中没有 nvcc，未发现 `/usr/local/cuda*`。前者代表驱动支持范围，不能当成已安装 Toolkit 版本。
- 选择 Python 3.12、vLLM 0.33.0（PyPI 2026-11-02 发布的稳定包）、其明确要求的 torch 2.14.0。PyPI 中 torch 2.14.0 声明 CUDA Toolkit 13.0.3 组件依赖；实际运行时版本由安装后验证决定。
- NVIDIA 官方 CUDA 兼容表要求 CUDA 13.x 驱动 >=580；595.99.02 满足。RTX 4090 为 Ada，预计算力 8.9，安装后读取确认。
- 使用 Conda 仅创建 Python/pip 基础环境，PyTorch/CUDA 库由 vLLM 的 pip 依赖统一解析，不另外用 Conda 安装 PyTorch 或全局 CUDA Toolkit。
- 显式前缀 `/data/xxx/conda/envs/vllm`；缓存 `/data/xxx/cache/{conda-pkgs,pip}`；记录 `/data/xxx/setup_records/exp_1112_02_vllm_environment`。
- Conda 使用 conda-forge，仅本次 `--override-channels`，不更改全局源或已有 envs_dirs。新前缀在初检时不存在。
- 无对应 repos/ 子项目：此项只创建环境，没有需要修改的子仓库，所以子项目分支／提交步骤不适用。父项目不执行 add/commit，不更改已有暂存选择。
- 基础验证：pip check，8 卡识别，GPU 0 小矩阵计算，vLLM CUDA 扩展导入及 SiLU CUDA 算子对照；不下载模型或启动推理服务。

## 资料

- https://pypi.org/pypi/vllm/0.33.0/json
- https://pypi.org/pypi/torch/2.14.0/json
- https://docs.vllm.ai/en/stable/getting_started/installation/gpu/
- https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html
- 当前官方安装页部分文字仍写默认 CUDA 12.9，与 PyPI torch 2.14.0 的 13.0.3 依赖不一致；以固定版本包元数据和实际 GPU 验证为准，不混用两个运行时的 PyTorch 构建。
- 按 AGENTS.md 尝试用本机 gh 查看发布记录，但本机 gh 未登录；没有登录或保存令牌，改用 PyPI 元数据及官方安装文档完成版本核对。

## 安装期间补查镜像与连通性

- 用户追问后完整读取 `default_channels`、`custom_channels`：已有 defaults→清华镜像、conda-forge/pytorch→清华镜像、nvidia→南科大镜像的映射。`channels: defaults` 本身不代表没有镜像。
- 本次 Conda 显式提供完整官方 URL `https://conda.anaconda.org/conda-forge`，pip 显式使用 `https://pypi.org/simple`；不依赖上述短名称映射，也没有修改持久配置。
- 在正在运行的服务器回环代理 `127.0.0.1:18797` 上并行测试：官方 Conda 元数据与 PyPI 索引 HTTP 200；files.pythonhosted.org 根路径返回 HTTP 404，说明 HTTPS 可达，但根路径不是包文件；Hugging Face 与 Google 本次 4 秒连接时限下 TLS 超时。没有据此推断所有域名或长期可用性。
- Wi-Fi 直连可访问安装所需源，不提供绕过网络访问限制的代理节点；后续模型下载的连通性不在本次基础安装验证范围。

## 临时镜像切换

- 初次 pip 正常解析依赖但很慢。对同一个 vLLM 0.33.0 wheel 的前 1 MiB 做 Range 测速：官方站 15 秒收到 339,686 字节（22,646 B/s），清华镜像 1.012 秒收到完整 1,048,576 字节（1,036,332 B/s）。
- 仅终止这次明确匹配 `/data/xxx/conda/envs/vllm/bin/python -m pip install` 的进程，保留成功创建的 Python 3.12.16 环境。初次 install.log 中的 SIGTERM/143 为主动换源，不是依赖安装错误。
- 安装脚本改为本次 `--index-url https://pypi.tuna.tsinghua.edu.cn/simple`，固定 vLLM 0.33.0，不修改 pip 全局配置。可通过单次环境变量 VLLM_PIP_INDEX_URL 切换回官方源。

## CUDA 编译工具约束

- 默认解析虽然将 cudart / nvrtc 回退到 13.0，但 humming-kernels 的宽松依赖仍选中了 nvcc / nvvm / nvjitlink 13.5，以及更新的 cuda-bindings。NVIDIA 官方说明较新 PTX 在旧驱动上有兼容限制，因此不能仅看运行时主版本相同。
- 增加 `cuda-constraints.txt`，按照 CUDA Toolkit 13.0.3 包元数据约束 nvcc / nvvm / crt / nvrtc 为 13.0.88 系列、CCCL 13.0.85 系列、cudart 13.0.96 系列，并选择 13.0.88 的 nvjitlink 和 13.0.3 的 Python bindings。
- 等首次 pip 安装事务完成后再应用约束，不在写入环境时中止 pip。最终验证增加实际 Triton JIT kernel 计算，缓存限定在个人目录。
- 首次 pip 安装和 pip check 成功，GPU 识别与矩阵检查也通过；验证脚本使用旧扩展名 `vllm._C` 报 ModuleNotFoundError。核对实际安装文件后确认本版本使用 `_C_stable_libtorch.abi3.so`，验证改为调用本版本的 `current_platform.import_kernels()`，随后执行真实算子，不能把旧模块名不存在当成安装包缺失。

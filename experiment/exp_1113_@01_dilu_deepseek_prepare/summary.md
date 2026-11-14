# DiLu 导入与 DeepSeek API 准备

完成 `@2024_ICLR_DiLu` 官方源码导入、独立初始化提交、最小 Windows 运行环境和 DeepSeek 适配。真实 API 和完整记忆增强流程尚未测试。使用命令见 [notes.md](notes.md)。

## 来源与版本

- 上游：<https://github.com/PJLab-ADG/DiLu>，`main`，`74c4aa96a8f5816731d5eb5cc1d93add30674287`。
- 固定提交归档通过 `C:\Program Files\GitHub CLI\gh.exe` 下载；28 个文件全部纳入本地初始化提交，逐字节比对没有差异，包括上游 `.gitignore` 排除的图像、配置和记忆库。
- 归档 SHA-256：`d28ccb23e080f631a8c436784ab49f8115b09af7d0186c35d1e216b41229b7ef`。
- 子项目：`repos/DiLu`，独立 Git 历史，`upstream` 指向官方地址。
- 初始化提交：`fb6e5fc`，`初始化：导入 DiLu 官方原始源码（74c4aa9）`。
- 改进提交：`89bcb3f`，`改进：准备 DeepSeek 接口、固定种子与离线复现检查`。完整记录见 `logs/git-log.txt` 及子项目 Git 历史。
- 当前实验分支：`exp_1113_@01_dilu_deepseek_prepare`。未开始正式 API 实验，因此保留两个提交及实验分支；父项目没有暂存或提交。

## 环境与改动

- 本机 Conda 环境 `dilu_py310`，实际路径 `D:\AppData\miniconda\envs\dilu_py310`，Python 3.10.22。
- 使用 `requirements-deepseek.txt`，沿用上游 LangChain 0.0.335、OpenAI 0.28.1、Highway-env 1.8.2、Gymnasium 0.28.1，固定 MoviePy 1.0.3 以配合旧视频接口。完整已安装版本见 `logs/pip-freeze.txt`。
- 聊天和反思默认基于 DeepSeek 实现；API 密钥统一通过 `repos/DiLu/.env` 单一入口读取（由 `.gitignore` 排除，绝不进入 Git），`config.yaml` 中彻底剔除任何密钥字段；默认启动模型为 `deepseek-chat`，显式禁用 thinking，默认温度 0、请求超时 60 秒、最多 2 次 SDK 重试。反思不再写死 GPT-4。
- 默认直接读取 `config.yaml`（已移除多余的 `config.deepseek.example.yaml`），保持官方原版的 DiLu 与 Highway-env 仿真参数（`few_shot_num: 3`、`episodes_num: 3`、`simulation_duration: 20` 等），仅在模型接口部分替换为 DeepSeek。检索/反思可另配独立 Embedding 地址、密钥和模型，尚未安装/验证其运行依赖。
- 显式输出目录、非空目录拒绝覆盖、离线单步入口、运行元数据；修正 Gymnasium 结束信号处理，并启用离屏渲染。原始提示词、动作空间及道路设置保持上游逻辑。

## 验证结果

1. `python -m pip check` 通过，无依赖冲突。
2. `python -m unittest discover -s tests -v`：4/4 通过。使用 mock 检查旧 SDK 最终收到的 DeepSeek 地址、模型、流式开关、thinking 参数、反思模型选择及缺失密钥报错，不进行外部请求。
3. 真实 Highway-env 离线仿真：种子 5838，1 个场景、1 个 IDLE 动作步骤，正常结束。SQLite 包含场景种子、1 条提示记录、10 条车辆记录；视频成功生成，首帧 600×150，像素范围 0–255。此项是运行与文件检查，没有评价模型驾驶能力。
4. 复用非空目录和向子项目写结果均被拒绝；缺少密钥时在创建输出目录前报错。
5. API 调用数 0；没有驾驶成功率、泛化能力或论文结果复现结论。

原始输出与检查：`logs/api-tests.log`、`logs/offline-smoke.log`、`logs/offline_01/`、`logs/artifact_checks.json`、`logs/upstream_verification.json`。

## 安装与检查过程中的问题

- `gh repo view` 因未登录不可用，使用 gh 访问公开 GitHub 网页确认分支和提交，并下载固定提交归档，没有进行登录或保存令牌。
- 首次 pip 运行经 Conda 包装而缓冲输出，下载 FFmpeg 时进度不可见。中止该次安装后，从相同环境直接执行 pip，复用缓存并保存实时日志；没有改动全局 Conda/pip 源。
- 初版 mock 测试清空整个进程环境，在 Windows 下移除了 SSL 所需系统变量。修正为只隔离 API 相关变量，保留 SystemRoot 等系统配置后测试通过；真实离线仿真不受此问题影响。

正式复现前应先执行一个真实 DeepSeek 小样本，再单独验证与原记忆库嵌入空间一致的检索路径；目前的零样本结果不能代替完整 DiLu 方法测试。

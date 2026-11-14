# DiLu DeepSeek 准备说明

论文统一称为 `@2024_ICLR_DiLu`。本次仅导入项目、准备 Windows 环境和 DeepSeek 接口，做离线检查；没有正式 API 评测。

## 启动方式

以下命令从父项目 `D:\Workspace\00_MyRepo\LLM_drive_research` 执行。独立 Conda 环境为 `dilu_py310`，依赖声明为 `repos/DiLu/requirements-deepseek.txt`。

重新安装时：

```powershell
conda create -n dilu_py310 python=3.10 pip -y --override-channels -c https://repo.anaconda.com/pkgs/main
conda run -n dilu_py310 python -m pip install -r repos/DiLu/requirements-deepseek.txt
```

离线仿真（直接使用默认 `repos/DiLu/config.yaml`，输出目录每次使用新的名字）：

```powershell
conda run --no-capture-output -n dilu_py310 python repos/DiLu/run_dilu.py --offline-smoke --output experiment/exp_1113_@01_dilu_deepseek_prepare/logs/offline_manual
```

之后的真实 API 小样本命令如下。本次没有执行；正式开新实验时先按通用原则创建对应目录、time.md 和同名分支，并将输出路径改到新实验下。默认 1 个场景、种子 5838、最多 3 个驾驶决策步骤；正常最多 3 次主要聊天请求，格式修复和失败重试会增加请求数。

密钥配置方式（单一入口，直接写入 `.env` 文件，由 `.gitignore` 排除，避免被 Git 追踪）：
在 `repos/DiLu/.env` 中配置：
```bash
DEEPSEEK_API_KEY=sk-xxxxxx
```

```powershell
# .env 配置完成后直接运行（默认读取 repos/DiLu/config.yaml，从 repos/DiLu/.env 读 Key）：
conda run --no-capture-output -n dilu_py310 python repos/DiLu/run_dilu.py --output experiment/exp_1113_@01_dilu_deepseek_prepare/logs/api_manual
```

`DEEPSEEK_BASE_URL` 默认为 `https://api.deepseek.com`，默认启动模型为 `deepseek-chat`。驾驶决策和反思共用接口配置，反思默认使用当前聊天模型，也可通过 YAML 的 `REFLECTION_MODEL` 单独指定。沿用上游旧 LangChain/OpenAI SDK，显式关闭 DeepSeek thinking，保持原有“文本推理 + #### 动作编号”的响应方式。接口格式与模型名核对日期：2026-11-13；来源：[DeepSeek 官方调用说明](https://api-docs.deepseek.com/)。

## 记忆模块与配置边界

- `config.yaml` 保持官方原版默认的 DiLu 设置（`few_shot_num: 3`、`episodes_num: 3`、`simulation_duration: 20` 等），仅在模型部分替换为 DeepSeek。零样本离线验证可通过 `--offline-smoke` 运行。
- 上游附带 `memories/20_mem`（原始记忆库及既有向量），已经纳入初始化提交。没有重新嵌入或改写它。
- 使用检索/反思时需额外安装兼容的 Chroma（上游为 `chromadb==0.3.29`）及依赖，并设置独立的 `DILU_EMBEDDING_API_KEY`。默认 Embedding 地址为 `https://api.openai.com/v1`、模型为 `text-embedding-ada-002`；可通过 `DILU_EMBEDDING_API_BASE` / `DILU_EMBEDDING_MODEL` 调整。查询向量必须与已有记忆使用同一嵌入空间；不能因为维数相同就直接更换模型。
- 本次未安装/验证 Chroma、Gradio、记忆检索和交互式反思；完整复现前需单独验证。启用反思后生成的新记忆保存在本次输出目录的 `memory_updated/`。

## 运行与记录

- `--output` 必须位于父项目 `experiment/` 内，拒绝复用非空目录，避免覆盖旧结果。
- `seeds` 控制场景初始化；未配置则沿用上游随机抽种子方式。固定场景种子不保证远端模型输出完全确定；模型实际版本和返回值以后应随真实 API 实验记录。
- 保留上游提示词和驾驶决策流程；修正 Gymnasium 的 terminated/truncated 接收顺序，显式注册 Highway-env，避免把时间截断当作碰撞。
- `run_info.json` 记录运行模式、模型、场景种子、零/少样本与反思设置；原有 SQLite、视频、log.txt 写入同一输出目录。
- 离线 IDLE 仿真仅检查环境、场景描述、数据库和视频，不测模型驾驶能力。本次 SDK 测试使用 mock，不发送网络请求，不产生 API 费用。
- 本次保留实验分支。通用原则中的 squash/main 合并在准备正式实验前执行；当前按用户要求保留“原始初始化”和“额外改进”两个提交。

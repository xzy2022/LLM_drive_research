# 实验 01 笔记与历史特殊情况

## 当时的配置

使用仓库内修改过的 `highway_env/`，没有安装 PyPI 同名包。仅安装 Zero-shot / Few-shot 所需依赖，未安装 Human Feedback、ChromaDB 和录像相关完整依赖，未下载本地模型权重。

依赖清单位于 `../../repos/LaMPilot/reproduction/requirements-win.txt`，完整历史锁文件位于同目录 `requirements-win.lock.txt`。安装时旧清华 `pkgs/pro` 源返回 404，创建环境时单次使用官方源，没有改动全局 Conda 配置。

## 当时遇到的问题

- 新版 LangChain 与官方旧接口不兼容的风险，通过固定版本处理。
- `SDL_VIDEODRIVER=dummy` 让上游 EnvViewer 禁用绘制，早期截图全黑；后改为 `offscreen_rendering=True`，保留动力学和评分代码。
- 离屏图像只在初始、最终状态保存，避免每步渲染。
- 官方数据加载器未直接给出论文独立测试集的 ID，因此只做固定 Demo 连通验证。

## 已有运行目录分类

| `logs/runs/` 子目录 | 含义 |
| --- | --- |
| `offline-smoke` | 最初诊断，截图为黑图，不作为最终图像证据 |
| `offline-verified` | 修正渲染后的中间验证 |
| `offline-validated` | 最终离线检查主记录 |
| `offline-timeout-check` | 人为设置 1 秒上限的预期超时记录 |
| `offline-wrapper-check` | Windows PowerShell 包装入口检查 |
| `_contract_checks` | 模拟 API HTTP 402 等异常；没有真实 API 请求 |

## 历史特殊情况

1. 当时未建立 `experiment/` 实验目录，没有记录三个规定时间；`time.md` 如实标缺失。
2. 没有对应的历史实验分支，也未按实验 squash。原模块提交保留，关联关系见 [提交对照](../commit_history.md)。
3. 运行入口同时支持离线和 API，代码提交与实验 02 有交叉，不能声称这两次历史实验有独立连续的提交范围。
4. 原始源码 ZIP 当前缺失。只保留 [来源和历史 SHA-256](logs/source/source.json) 及 Git 初始化源码，不补下载。
5. 安装过程、部分临时接口检查没有完整原始终端日志；旧说明和 Git 提交是现有旁证，本次不合成缺失日志。
6. 迁移前的 manifest 和旧文档均原样保存；其中的旧路径和旧 Git HEAD 代表当时状态，不替换成当前整理版本。

## 本次整理边界

只迁移和校验已有文件，并调整后续入口的输出目录约束。没有运行 `run.ps1` / `run_small.py`、调用 API、重装环境或补做上述检查。未来的新实验应先创建新的实验目录和同名分支，遵守父项目的实验通用原则。

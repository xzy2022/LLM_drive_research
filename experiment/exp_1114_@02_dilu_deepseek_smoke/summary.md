# DiLu DeepSeek 最小实验总结（Zero-Shot 闭环验证）

- **论文统一称呼**：`@2024_ICLR_DiLu`
- **实验代码仓库**：`repos/DiLu`
- **Git 提交哈希**：`8b4a0d2a8b56c94019ab9c49003d1825ca13ee4a`（`main` 分支）
- **实验环境**：Windows 11，Conda 环境 `dilu_py310`（Python 3.10.22）
- **调用模型**：`deepseek-chat`（DeepSeek-V3 官方 API）
- **凭据方式**：从 `repos/DiLu/.env` 唯一读取

## 1. 实验启动命令

```powershell
conda run --no-capture-output -n dilu_py310 python repos/DiLu/run_dilu.py --config experiment/exp_1114_@02_dilu_deepseek_smoke/config.yaml --output experiment/exp_1114_@02_dilu_deepseek_smoke/logs/run_01
```

## 2. 关键配置与 DeepSeek 参数设置

### 2.1 任务与仿真环境参数
- `episodes_num`: 1
- `simulation_duration`: 3 步决策
- `few_shot_num`: 0（Zero-Shot，不调用 Embedding，不依赖 Chroma 记忆库）
- `reflection_module`: False
- `seeds`: [5838]
- 交通环境：4 车道高速公路（`highway-v0`），车流密度 2.0，周边车辆数 15

### 2.2 DeepSeek API 调用关键参数
- **模型名称 (`model_name`)**: `deepseek-chat`
- **采样温度 (`temperature`)**: `0.0`（完全确定性输出，消除随机性漂移）
- **底层思考模式 (`thinking`)**: `{'type': 'disabled'}`（**显式禁用底层原生 Reasoning/Thinking 块**，纯标准文本输出）
- **最大输出 Token (`max_tokens`)**: `2000`（预留足够空间避免分析过程被截断）
- **请求超时与容错**: 单次超时 `60s`，SDK 失败自动重试上限 `2` 次
- **输出机制 (`streaming`)**: `True`（终端实时流式显示推导文本）

## 3. 提示词输入与模型输出边界划分

在 DiLu 交互循环中，输入与输出在底层有着严格的数据边界：

```
┌────────────────────────────────────────────────────────────────────────┐
│                        【输入边界：Python 代码生成】                   │
│                                                                        │
│ 1. System Prompt（系统协议定义）：                                     │
│    - 角色：成熟驾驶助手                                                │
│    - 规范：必须以 <reasoning> ... </reasoning> 进行显式文字分析        │
│    - 输出标记：必须以 Response to user:#### <Action_id> 结尾           │
│                                                                        │
│ 2. Human Prompt（单步场景数值文本化）：                                │
│    - #### Driving scenario description:（自车坐标/速度、关键邻车数据） │
│    - #### Driving Intensions: Drive safely and avoid collisons         │
│    - #### Available actions:（0~4 离散宏动作含义清单）                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ 发送至 DeepSeek
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        【输出边界：DeepSeek 生成正文】                 │
│                                                                        │
│ 1. 提示词引导的显式文字推导（Prompt-guided CoT）：                     │
│    <reasoning>                                                         │
│    排查前车逼近风险 -> 排查变道空间 -> 形成最终动作选择                │
│    </reasoning>                                                        │
│                                                                        │
│ 2. 物理动作触发行：                                                    │
│    Response to user:#### <Action_id>                                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Python 代码接收并解析
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        【执行边界：Python 提取与步进】                 │
│                                                                        │
│ Python 解析：                                                          │
│   decision_action = response.split("####")[-1]                         │
│   action = int(decision_action)  # 提取得到纯整数动作编号              │
│   env.step(action)               # 交付 Highway-env 进行下一物理周期   │
└────────────────────────────────────────────────────────────────────────┘
```

## 4. 实验定量结果与指标

| 评估指标 | 测量结果 | 指标含义与说明 |
| :--- | :--- | :--- |
| **任务状态** | **成功 (Success)** | 设定步数内无碰撞安全行驶 |
| **完成步数** | **3 步** | 跑满设定的 3 个决策周期 |
| **碰撞发生 (Collision)** | **否 (False)** | 未发生追尾或擦碰 |
| **行驶距离 (Traveled Distance, TD)** | **43.87 m** | 初始位置 $x=363.46$，结束位置 $x=407.33$ |
| **车速动态响应** | $25.00 \to 22.41 \to 19.17$ m/s | 遇前车急刹时果断制动避险 |
| **输出动作序列** | `[Deceleration, Deceleration, IDLE]` | 动作 ID 分别为 `[4, 4, 1]` |
| **API 调用次数** | 3 次成功，0 次格式重试 | 均一步通过，显式分析与格式标记 100% 正确 |

## 5. 产出文件

- 驾驶视频：`logs/run_01/highway_0-episode-0.mp4`（MP4，35.7 KB）
- 结构化数据库：`logs/run_01/highway_0.db`（SQLite，40.0 KB）
- 运行元数据：`logs/run_01/run_info.json`
- 执行记录：`logs/run_01/log.txt`

## 6. 结论

1. **链路完全闭环**：验证了 DeepSeek 驱动 DiLu 的完整通道（几何空间描述生成 $\to$ Prompt 组装 $\to$ 流式文字分析 $\to$ 动作提取 $\to$ 仿真器步进更新 $\to$ 视频/数据库存储）。
2. **决策因果合理**：DeepSeek 在 Zero-Shot 模式下依据提示词规范，在文字分析中准确捕获前方急刹险情（-6 m/s²）并连续执行制动；待前车变道让出净空后平稳恢复 IDLE 巡航。
3. **零额外开销与高稳健度**：纯 Zero-Shot 避免了 Chroma 与 Embedding API 依赖，单次实验仅消耗少量 Token，运行极为迅速且稳定。

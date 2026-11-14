# DiLu DeepSeek 长时程实验总结（30 步基准全闭环验证）

- **论文统一称呼**：`@2024_ICLR_DiLu`
- **实验代码仓库**：`repos/DiLu`
- **Git 提交哈希**：`ebe79c2e0bbf4e756c6d05fce949822a106fdf24`（`main` 分支）
- **实验环境**：Windows 11，Conda 环境 `dilu_py310`（Python 3.10.22）
- **调用模型**：`deepseek-chat`（DeepSeek-V3 官方 API）
- **凭据方式**：从 `repos/DiLu/.env` 唯一读取

## 1. 实验目标与时长设置依据

本实验（`@03`）在 `@02` 最小链路冒烟实验成功的基础上，保持所有核心参数不变，将仿真时长拉长，全面检验模型在更长时程、动态交通流下的持续驾驶决策稳定性与安全性。

### 时长设定：`simulation_duration: 30`（30 步决策 / 30 秒仿真）
- **依据来源**：[`@2024_ICLR_DiLu`](file:///D:/Workspace/00_MyRepo/LLM_drive_research/papers_md/@2024_ICLR_DiLu.md) 论文正文第 4.1 节、第 4.2 节及附录 A.1。
- **学术依据与原文定义**：
  1. **决策与仿真频率**：附录 A.1 明确定义决策频率为 $1\text{ Hz}$（1 步对应物理时间 1 秒）。
  2. **成功步数与完成标准**：正文第 4.1 节明确指出：*“Success Steps (SS) is the number of consecutive frames without collision, an SS of 30 means that the ego car has completed the driving task.”*（无碰撞行驶满 30 步即代表自车完成整个闭环驾驶测试任务）。
  3. **成功率判定**：正文第 4.2 节将成功率（Success Rate, SR）统一定义为连续 30 步无碰撞行驶。
  4. **对比基准**：代码仓库模板设置为了快速调试默认写了 20 步，而 **30 步是论文给出的唯一且严谨的基准上限**。在有据可依的数字中，30 步是最长且最具评测意义的完整标尺。

## 2. 实验启动脚本

```powershell
conda run --no-capture-output -n dilu_py310 python repos/DiLu/run_dilu.py --config experiment/exp_1114_@03_dilu_deepseek_long_run/config.yaml --output experiment/exp_1114_@03_dilu_deepseek_long_run/logs/run_01
```

## 3. 关键配置表

| 配置项 | 参数值 | 说明与依据 |
| :--- | :--- | :--- |
| **`simulation_duration`** | **`30`** | **对齐 ICLR 2024 论文完整评测上限（30 步 / 30 秒）** |
| `episodes_num` | 1 | 单场景评测 |
| `seeds` | `[5838]` | 保持与 `@02` 完全一致的初始交通流，确保长时程行为的可比性 |
| `few_shot_num` | 0 | Zero-Shot 模式（纯靠 Prompt 与预训练推理） |
| `reflection_module` | False | 禁用在线反思模块 |
| `OPENAI_CHAT_MODEL` | `deepseek-chat` | DeepSeek-V3 官方模型 |
| `temperature` | 0.0 | 确定性生成，避免随机性抖动 |
| `thinking` | `{'type': 'disabled'}` | 显式禁用模型原生 Reasoning 块，纯正文 Prompt-guided CoT |
| `vehicle_count` | 15 | 场景周边车辆总数 |
| `vehicles_density` | 2.0 | 高速公路高密度交通流 |

## 4. 实验核心定量结果

| 评估指标 | 测量结果 | 指标定义与学术意义 |
| :--- | :--- | :--- |
| **任务状态** | **成功 (Success)** | 达成论文设定的满步测试要求 |
| **完成步数 (SS)** | **30 / 30 步 (100%)** | 达到 `@2024_ICLR_DiLu` 满分上限（$SS = 30$） |
| **碰撞发生 (Collision)** | **0 次 (False)** | 全程 30 秒无任何擦碰与追尾 |
| **行驶总距离 (TD)** | **491.80 m** | 起始位置 $x=363.46\text{ m}$，结束位置 $x=855.26\text{ m}$ |
| **全程车速区间** | $15.13\text{ m/s} \sim 25.00\text{ m/s}$ | 平均速度 $17.10\text{ m/s}$（约 $61.6\text{ km/h}$） |
| **动作序列分布** | 3 次减速 (`4`)，27 次巡航 (`1`) | 无违背安全性的剧烈盲目加速或极限变道 |
| **API 调用统计** | 30 次调用，30 次首推通过 | 0 格式报错重试，格式解析成功率 100% |

## 5. 决策演进全时程三阶段分析

整个 30 步驾驶过程呈现出高度符合交通工程常识的三个清晰阶段：

```
Frame 00 ──(减速)──> Frame 01 ──(减速)──> Frame 02 ──────> Frame 12 ──(减速)──> Frame 13 ──────> Frame 29
   │                    │                    │                     │                    │
【阶段一：初期突发险情响应】                【阶段二：中段稳定巡航】           【阶段三：二次跟车调节与稳态巡航】
 前车 984 突发 -6 m/s² 紧急制动             前车让出车道，道路开阔               前车 856 减速逼近 (间距 31m)        匹配车流速度 (15.13 m/s)
 自车连续 2 轮减速避险 (25->19.17)          自车 IDLE 巡航 (18.5 m/s)           自车主动制动控距 (18.5->15.13)      自车平稳跟驰至终点
```

1. **阶段一（Frame 0 ~ 1）：突发急刹避险阶段**
   - 自车以 25 m/s 入场，同车道前车 984 突发 $-6.00\text{ m/s}^2$ 剧烈制动，车间距骤缩至 13.91 m。
   - DeepSeek 准确识别风险，连续下发 2 次 `Deceleration`（动作 ID 4），将车速从 25.00 m/s 降至 19.17 m/s，成功化解追尾危机。
2. **阶段二（Frame 2 ~ 12）：排空巡航阶段**
   - 前车 984 变道右侧离开本车道，新前车 856 距离较远（>26 m）且微加速。
   - DeepSeek 维持车道并执行 `IDLE` 巡航（动作 ID 1），车速在 Highway-env 物理阻力下收敛并稳定在 18.50 m/s，持续推进约 200 米。
3. **阶段三（Frame 13 ~ 29）：二次跟车控距与稳态巡航阶段**
   - 至 Frame 13，前车 856 出现轻微制动（$-0.37\text{ m/s}^2$），车间距缩小至 31 m 且相对速度缩小。
   - DeepSeek 在文字分析中评估了左右变道可行性，因左道车速过慢（13 m/s）、右后方来车较近，理性选择再次 `Deceleration`（从 18.50 m/s 进一步微调至 15.13 m/s）。
   - 随后的 Frame 14~29，自车速度与前车完全动态同步（间距维持在 35~45 米的安全平衡点），全线执行 `IDLE` 平稳跟车，直至 30 步圆满结束。

## 6. 图表与产出文件

- **行驶速度与动作曲线**：[speed_and_actions.png](figures/speed_and_actions.png)
- **纵向位移发展曲线**：[trajectory_profile.png](figures/trajectory_profile.png)
- **仿真驾驶完整视频**：`logs/run_01/highway_0-episode-0.mp4`（MP4 录像，451 帧渲染画面）
- **全量 SQLite 数据库**：`logs/run_01/highway_0.db`（记录 30 帧全部 Prompts、CoT 正文、周围车辆全量运动学信息）
- **运行元数据与日志**：`logs/run_01/run_info.json`、`logs/run_01/log.txt`

## 7. 结论

1. **长时程安全性验证达成**：在 `@2024_ICLR_DiLu` 的 30 步标准评测中，DeepSeek-V3 在 Zero-Shot 模式下无记忆库辅助即达成 **100% 任务完成度（$SS = 30$）** 与 **0 碰撞率**，总行驶里程达 **491.80 米**。
2. **决策具备纵向自适应跟驰能力**：模型不仅能应对初期突发紧急制动，还能在中长时程下根据前方车流的微弱减速动态，主动、平滑地介入二次制动以保持安全车距，避免了传统规则或单一策略在长时程累积下的速度失控或追尾。
3. **输出协议高度稳定**：连续 30 步无任何格式跳变或超时，完全满足长时间端到端在线闭环仿真的可靠性要求。

# 实验 04：GPT-6.1 Sol（低级思考模式）首样本验证与额度预估

- **实验项目**：`@2024_CVPR_LaMPilot-Bench`
- **Git 提交哈希**：`34b30b80db36248d91c13ef3d0246a4805e45a27`（分支 `exp_1107_@04_lampilot_gpt6.1sol_test` 压缩合并至 `main`）
- **实验环境**：Windows 11，Conda `lampilot_py311`，Python 3.11.18，RTX 5060 Laptop (8GB)
- **启动脚本**：
  ```powershell
  powershell -ExecutionPolicy Bypass -File repos/LaMPilot/reproduction/run.ps1 -Mode api -Model gpt6.1sol -Dataset table3 -Limit 1 -Output experiment/exp_1107_@04_lampilot_gpt6.1sol_test/logs/runs/gpt6.1sol-one
  ```
- **模型配置**：`gpt-6.1-sol`（别名 `gpt6.1sol`），`reasoning_effort="low"`（低级思考模式），原版 3-shot 提示词（`prompts/cg_template_fs.txt`），依据 OpenAI 推理模型规范剔除 `temperature`。
- **评测样本**：Table 3 评测集首个样本 `dec_abs_dis15_s0_c0`。

---

## 1. 单样本运行结果

| 指标 | 实际数值 | 说明 |
| :--- | :---: | :--- |
| **测试样本** | `dec_abs_dis15_s0_c0` | 任务：将跟车距离缩减至 15 米 |
| **API 响应状态** | **成功 (200 OK)** | 模型正常识别并返回完整策略 |
| **代码解析状态** | **成功 (100%)** | 官方 Python 解析器成功提取生成函数 |
| **仿真执行状态** | **完成 (Completed)** | 仿真完整运行 60.1 秒，墙钟耗时 13.5 秒 |
| **碰撞状态** | **无碰撞 (0 碰撞)** | 始终保持安全行车 |
| **官方评分器判定** | **False (未达标)** | 自车未能在 60 秒内连续 5 秒维持目标距离 |
| **输入 Token** | 2,637 | 包含系统原语与 3-shot 示例 |
| **输出 Token** | 354 | 含自然语言 Plan 与 Python 代码 |
| **总 Token** | 2,991 | 单次调用消耗 |

---

## 2. 策略代码特性对比分析

### DeepSeek 生成逻辑（实验 03 首样本）：
```python
def decrease_gap_to_15_meters():
    ego = get_ego_vehicle()
    current_lane = get_lane_of(ego)
    desired_gap = 15
    while True:
        front_vehicle = detect_front_vehicle_in(current_lane)
        if front_vehicle is not None:
            # 机械仿照 3-shot 示例，步长 0.05 持续死循环调节
            ...
            yield autopilot()
        else:
            return
```
- 特点：完全复刻官方 3-shot 模板的 `while True:` 调节循环，无论是否达到 15 米都保持步进，在 `s0_c0` 恰好碰运气维持了 5 秒判定成功。

### GPT-6.1 Sol 生成逻辑（本次实验）：
```python
def decrease_gap_to_15_meters():
    ego = get_ego_vehicle()
    lane = get_lane_of(ego)
    front = detect_front_vehicle_in(lane)
    desired_gap = 15.0
    ...
    for step in range(300):
        gap = get_distance_between_vehicles(front, ego)
        if 14.0 <= gap <= 16.0:
            say('The following gap is approximately 15 meters.')
            return  # <--- 达到区间即主动 exit
        headway = get_desired_time_headway()
        if gap > desired_gap:
            if headway > 0.6:
                set_desired_time_headway(max(0.6, headway - 0.02))
        else:
            set_desired_time_headway(headway + 0.05)
        yield autopilot()
```
- **关键发现**：
  1. **自主工程优化**：GPT-6.1 Sol 自主加入了安全保护（`headway > 0.6` 下限保护、更平缓的缩小步长 `0.02`、最大步数限制 `range(300)`）。
  2. **提早退出陷阱**：它设置了 `if 14.0 <= gap <= 16.0: return`。当距离进入目标区间时，它认为“任务已完成”并主动退出了函数；但官方评测器（`ACCEvalbyDistance`）要求**自车必须在区间内连续保持 5 秒**。函数提前返回导致自车失去主动控制，无法完成评测器苛刻的 5 秒稳态计时。

---

## 3. 全量测试（98 样本）额度与费用预估

依据 OpenAI 官方公布的 `gpt-6.1-sol` API 定价：
- **标准输入**：$2.00 / 100 万 tokens
- **缓存输入**：$0.10 / 100 万 tokens
- **输出**：$10.00 / 100 万 tokens

### 费用核算：

| 场景 | 输入费用 | 输出费用 | 合计费用 (USD) | 折合人民币 (CNY) |
| :--- | :---: | :---: | :---: | :---: |
| **单样本实际支出** | $0.0053 | $0.0035 | **~$0.0088** | **约 0.063 元** (6分钱) |
| **98 样本全量预估 (缓存生效)** | ~$0.058 | ~$0.343 | **~$0.40** | **约 2.88 元** |
| **98 样本最坏情况 (无缓存)** | ~$0.517 | ~$0.343 | **~$0.86** | **约 6.20 元** |

**结论**：全量测试 98 个样本的预计总花费在 **0.4 美元（约 2.9 元人民币）** 左右，成本极低。

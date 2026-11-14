# 实验 03 笔记与深度剖析

## 1. 实验思路与设计决策

1. **放弃 HF 版本的依据**：
   - 原项目 `test_hf.py` 内部硬编码了终端人工交互 `input()`，无法自动化无缝运行。
   - 官方未开源预构建的向量库与 policy checkpoint。
   - `PolicyRepository` 强依赖 `OpenAIEmbeddings`，而 DeepSeek 官方 API 不具备 Embedding 端点。
   - 因此按照用户决策，先落地最具横向对比价值的 Table 3 核心基线：**3-shot Few-shot 评测**。
2. **测试集口径对齐**：
   - 依据 `docs/人类认知和术语对齐/LaMPilot测试划分与论文结果.md` 的反推与复核，论文 Table 3 的 Few-shot 报告值 84.7%（83/98）并非全量 4900 或 500 测试集，而是仓库默认的 98 个样本。
   - 这 98 个样本全部来自单一任务配置 `dec_abs_dis15`（包含场景 `s0`–`s9` 的全部 10 个场景及指令改写）。
   - 本次实验严格以该 98 个样本为评测范围，保证评估口径与分母与论文完全一致。

---

## 2. 关键配置与工程适配

1. **入口扩展**：
   - 在子仓库 `reproduction/run_small.py` 和 `reproduction/run.ps1` 中新增 `--dataset table3` 选项，支持按配置加载 `DbLv1Dataset` 的前 98 个样本。
   - 保留了小进程隔离沙箱（每个样本独立 worker 子进程），有效防止单个环境因超时或 SDL 离屏渲染句柄泄漏污染主进程。
2. **规范执行**：
   - 在分支 `exp_1107_@03_lampilot_deepseek_3shot` 上先执行首样本（`dec_abs_dis15_s0_c0`）单步预检，验证通过后通过 `git merge --squash` 合并回 `main` 分支并清理临时分支。
   - 严格记录 `time.md` 中的三个时间点（接入时间 22:40:15、启动时间 22:42:41、分析时间 23:01:01）。

---

## 3. 踩过的坑与失败归因剖析

### 为什么 DeepSeek 只有 45.92%，而 GPT-4 有 84.7%？
深入检查所有 53 个失败样本的代码与仿真轨迹发现：
1. **官方 Few-shot 示例的负反馈缺陷**：
   官方示例（`prompts/cg_template_fs.txt`）采用了一种朴素的 Bang-bang 控制：
   ```python
   if current_gap > desired_gap:
       set_desired_time_headway(current_time_headway - 0.05)
   else:
       set_desired_time_headway(current_time_headway + 0.05)
   yield autopilot()
   ```
   每个仿真步长为 0.1s，意味着每 1 秒内 headway 变化可达 $\pm 0.5s$。对于 IDM 模型，headway 的微小变化就会引起加速度的剧烈变动。
2. **评测器的苛刻稳态判定**：
   官方评测器（`ACCEvalbyDistance`）要求自车在目标距离 $\pm 30\%$（即 $[10.5m, 19.5m]$）区间内**连续维持 5.0 秒**。只要在 5 秒中有任何一个步长冲出区间，计时器就会清零（`self.last_time = -1`）。
3. **DeepSeek 的模仿倾向**：
   DeepSeek 非常忠实地仿照了提示词示例中的逻辑结构（甚至连步长 0.05 都保持一致），导致在长距离追车或前车低速场景（如 `s4`、`s7`）中，自车逼近目标后出现持续的正弦振荡，不断在 10.5m~19.5m 边缘反复横跳，直到 60 秒上限触发失败。
4. **零碰撞但保守**：
   53 个失败中，0 碰撞，100% 均为超时。这表明 DeepSeek 能够保证绝对安全距离，但在控制收敛性（控制理论中的阻尼与积分稳定性）上受限于示例给出的简陋启发式逻辑。

---

## 4. 后续研究与改进空间（潜在担忧）

1. **Few-shot Prompt 对代码生成上限的制约**：
   如果提示词给出的 Example 存在控制振荡缺陷，强模型也倾向于“拟合”示例模式。如果加入 PID 或带死区（deadband）的平滑控制示例，DeepSeek 的完成率有望大幅跃升。
2. **HF（记忆/检索）机制的价值预期**：
   正因为 3-shot 缺乏自适应调整能力，论文作者引入的 Human Feedback（或记忆反思库）能够针对震荡失败给出 critique 并固化成功策略。这解释了为什么论文中 HF 版本能将成绩从 84.7% 进一步推高至 92.7%。

import sqlite3
import os
import matplotlib.pyplot as plt

os.makedirs('experiment/exp_1114_@03_dilu_deepseek_long_run/figures', exist_ok=True)
db_path = r'experiment/exp_1114_@03_dilu_deepseek_long_run/logs/run_01/highway_0.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Prompts and actions
prompts = cur.execute("SELECT decisionFrame, done, thoughtsAndAction FROM promptsINFO ORDER BY decisionFrame").fetchall()
actions = []
for r in prompts:
    lines = [line.strip() for line in r[2].strip().split('\n') if line.strip()]
    last_line = lines[-1] if lines else "None"
    action_val = int(last_line.split("####")[-1].strip()) if "####" in last_line else 1
    actions.append((r[0], action_val))

# Veh info for ego
ego_rows = cur.execute("SELECT decisionFrame, vehicleID, speed, acceleration, laneIndexI, posx, posy FROM vehINFO WHERE vehicleID='ego' ORDER BY decisionFrame").fetchall()
frames = [r[0] for r in ego_rows]
speeds = [r[2] for r in ego_rows]
pos_x = [r[5] for r in ego_rows]
accs = [r[3] for r in ego_rows]

# 1. Speed and Action Profile Plot
plt.figure(figsize=(10, 5), dpi=200)
plt.plot(frames, speeds, color='#1f77b4', linewidth=2.2, label='Ego Speed (m/s)', marker='o', markersize=4)
for frame_idx, act in actions:
    if act == 4:  # Deceleration
        plt.scatter(frame_idx, speeds[frame_idx], color='#d62728', s=120, zorder=5, label='Deceleration Action (4)' if frame_idx == 0 else "")
        plt.annotate(f"Decel\n(Frame {frame_idx})", xy=(frame_idx, speeds[frame_idx]), xytext=(frame_idx, speeds[frame_idx] + 1.2),
                     ha='center', fontsize=9, fontweight='bold', color='#d62728',
                     arrowprops=dict(arrowstyle='->', color='#d62728', lw=1.2))
    elif act == 1 and frame_idx in [2, 14]:  # Transitions to IDLE
        plt.scatter(frame_idx, speeds[frame_idx], color='#2ca02c', s=90, zorder=5, label='IDLE Cruise (1)' if frame_idx == 2 else "")

plt.title('Ego Vehicle Speed Profile & Actions over 30 Decision Frames (DiLu + DeepSeek-V3)', fontsize=13, fontweight='bold')
plt.xlabel('Decision Frame / Time (seconds)', fontsize=11)
plt.ylabel('Speed (m/s)', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.ylim(12, 28)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('experiment/exp_1114_@03_dilu_deepseek_long_run/figures/speed_and_actions.png')
plt.close()

# 2. Distance & Position Profile Plot
plt.figure(figsize=(10, 5), dpi=200)
plt.plot(frames, pos_x, color='#ff7f0e', linewidth=2.2, label='Ego Longitudinal Position X (m)', marker='s', markersize=4)
plt.title('Ego Vehicle Longitudinal Traveled Distance over 30 Frames (Total = 491.80 m)', fontsize=13, fontweight='bold')
plt.xlabel('Decision Frame / Time (seconds)', fontsize=11)
plt.ylabel('Position X (m)', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('experiment/exp_1114_@03_dilu_deepseek_long_run/figures/trajectory_profile.png')
plt.close()

print("Figures generated successfully!")

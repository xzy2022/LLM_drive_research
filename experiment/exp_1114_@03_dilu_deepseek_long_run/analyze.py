import sqlite3
import os
import sys

db_path = r'experiment/exp_1114_@03_dilu_deepseek_long_run/logs/run_01/highway_0.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    sys.exit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("=== PROMPTS & DECISION SUMMARY ===")
prompts = cur.execute("SELECT decisionFrame, done, thoughtsAndAction FROM promptsINFO ORDER BY decisionFrame").fetchall()
actions = []
for r in prompts:
    lines = [line.strip() for line in r[2].strip().split('\n') if line.strip()]
    last_line = lines[-1] if lines else "None"
    action_val = last_line.split("####")[-1].strip() if "####" in last_line else "unknown"
    actions.append(action_val)
    print(f"Frame {r[0]:02d} (Done={r[1]}): Action={action_val}")

print(f"\nTotal Frames Executed: {len(prompts)}")
print("Action sequence:", actions)

print("\n=== EGO VEHICLE TRAJECTORY ===")
ego_rows = cur.execute("SELECT decisionFrame, vehicleID, speed, acceleration, laneIndexI, posx, posy FROM vehINFO ORDER BY decisionFrame, vehicleID").fetchall()
# Ego vehicle is located at (363.46, 8.00) at Frame 0
ego_id = None
for r in ego_rows:
    if r[0] == 0 and abs(r[5] - 363.46) < 0.1:
        ego_id = r[1]
        break

print(f"Detected Ego vehicleID: {ego_id}")
start_x, end_x = None, None
speeds = []
for r in ego_rows:
    if r[1] == ego_id:
        if start_x is None:
            start_x = r[5]
        end_x = r[5]
        speeds.append(r[2])
        print(f"Frame {r[0]:02d}: Speed={r[2]:.2f} m/s, Acc={r[3]:.2f} m/s^2, Lane={r[4]}, Pos=({r[5]:.2f}, {r[6]:.2f})")

traveled_distance = (end_x - start_x) if (start_x is not None and end_x is not None) else 0.0
print(f"\n=== METRICS SUMMARY ===")
print(f"Total Decision Steps: {len(prompts)}")
print(f"Traveled Distance (TD): {traveled_distance:.2f} m")
print(f"Start Pos X: {start_x:.2f} m, End Pos X: {end_x:.2f} m")
if speeds:
    print(f"Min Speed: {min(speeds):.2f} m/s, Max Speed: {max(speeds):.2f} m/s, Avg Speed: {sum(speeds)/len(speeds):.2f} m/s")

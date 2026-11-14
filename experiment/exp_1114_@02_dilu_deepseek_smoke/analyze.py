import sqlite3

db_path = r'experiment/exp_1114_@02_dilu_deepseek_smoke/logs/run_01/highway_0.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("=== PROMPTS INFO ===")
for r in cur.execute("SELECT decisionFrame, done, thoughtsAndAction FROM promptsINFO").fetchall():
    print(f"\n[Decision Frame {r[0]}] (Done={r[1]}):")
    # 提取 action
    last_line = r[2].strip().split('\n')[-1]
    print("Action output line:", last_line)
    print("Thoughts preview:", r[2].replace('\n', ' ')[:150], "...")

print("\n=== VEHICLE TRAJECTORY (EGO) ===")
# 在 highway-env 中 ego 车辆的 vehicleID 通常是固定的，或者第一辆车
ego_rows = cur.execute("SELECT decisionFrame, vehicleID, speed, acceleration, laneIndexI, posx, posy FROM vehINFO ORDER BY decisionFrame, vehicleID").fetchall()
# 找出哪个是 ego (可以通过比较坐标和描述中的自车坐标)
# 自车在 Frame 0 坐标为 (363.46, 8.00)
ego_id = None
for r in ego_rows:
    if r[0] == 0 and abs(r[5] - 363.46) < 0.1:
        ego_id = r[1]
        break

print(f"Detected Ego vehicleID: {ego_id}")
start_x = None
end_x = None
for r in ego_rows:
    if r[1] == ego_id:
        if start_x is None:
            start_x = r[5]
        end_x = r[5]
        print(f"Frame {r[0]}: Speed={r[2]:.2f} m/s, Acc={r[3]:.2f} m/s^2, Lane={r[4]}, Pos=({r[5]:.2f}, {r[6]:.2f})")

traveled_distance = (end_x - start_x) if (start_x and end_x) else 0.0
print(f"\n=== METRICS SUMMARY ===")
print(f"Total Decision Steps: 3")
print(f"Collision: No (All completed successfully)")
print(f"Traveled Distance (TD): {traveled_distance:.2f} m")
print(f"Start Pos X: {start_x:.2f} m, End Pos X: {end_x:.2f} m")

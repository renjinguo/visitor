import sqlite3

# 连接到数据库
conn = sqlite3.connect('visitor.db')
conn.row_factory = sqlite3.Row  # 使结果可以通过列名访问
cursor = conn.cursor()

# 查询所有访客数据
cursor.execute("SELECT * FROM visitors")
visitors = cursor.fetchall()

# 显示数据
print(f"共有 {len(visitors)} 条访客记录：\n")
print("ID  | 姓名  | 身份证号        | 电话         | 来访目的   | 登记时间            | 开始时间            | 结束时间")
print("-" * 120)

for visitor in visitors:
    print(f"{visitor['id']:<4}| {visitor['name']:<5}| {visitor['id_number']:<15}| {visitor['phone']:<12}| {visitor['purpose']:<8}| {visitor['visit_time']:<20}| {visitor['start_time']:<20}| {visitor['end_time']}")

conn.close()
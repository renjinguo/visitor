import sqlite3

conn = sqlite3.connect('visitor.db')
cursor = conn.cursor()

# 获取所有表名
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("数据库中的表:", [table[0] for table in tables])

# 如果有表，显示每个表的结构
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print(f"\n表 '{table_name}' 的结构:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")

conn.close()
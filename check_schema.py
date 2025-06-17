import sqlite3

conn = sqlite3.connect('visitor.db')
cursor = conn.cursor()

# 获取表结构
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='visitor'")
schema = cursor.fetchone()
if schema:
    print("visitor表结构:")
    print(schema[0])
else:
    print("visitor表不存在")

conn.close()
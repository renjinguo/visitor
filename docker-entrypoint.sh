#!/bin/sh

# 初始化数据库（如果不存在）
if [ ! -f /app/data/visitor.db ]; then
    echo "Initializing database..."
    python init_db.py
fi

# 启动Flask应用
exec python app.py

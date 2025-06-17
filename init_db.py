import sqlite3
import hashlib
import os
from datetime import datetime

def hash_password(password):
    """使用 SHA-256 对密码进行哈希"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """初始化数据库并创建默认管理员账户"""
    # 获取数据库路径
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'visitor.db')
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    db = conn.cursor()
    
    # 读取并执行 schema.sql
    with open('schema.sql', 'r', encoding='utf-8') as f:
        db.executescript(f.read())
    
    # 创建默认管理员账户
    admin_username = 'admin'
    admin_password = hash_password('admin123')  # 默认密码：admin123
    admin_email = 'admin@example.com'
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 插入管理员账户
    try:
        db.execute(
            'INSERT INTO system_users (username, password, email, created_at) VALUES (?, ?, ?, ?)',
            (admin_username, admin_password, admin_email, created_at)
        )
        conn.commit()
        print('成功创建数据库并添加默认管理员账户')
        print(f'用户名: {admin_username}')
        print(f'密码: admin123')
        print('请登录后立即修改默认密码！')
    except sqlite3.IntegrityError:
        print('管理员账户已存在，跳过创建')
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
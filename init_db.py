from app import app, init_db

with app.app_context():
    init_db()
    print("数据库初始化成功！")

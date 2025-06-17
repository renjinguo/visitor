from app import app, get_db
import datetime

# 示例数据
sample_visitors = [
    # 本月数据 (6月1日)
    {
        "name": "张三",
        "id_number": "110101199001011234",
        "phone": "13800138001",
        "purpose": "商务会议",
        "visit_time": "2025-06-01 09:30:00",
        "start_time": "2025-06-01 10:00:00",
        "end_time": "2025-06-01 11:30:00"
    },
    {
        "name": "李四",
        "id_number": "110101199102022345",
        "phone": "13900139002",
        "purpose": "设备维修",
        "visit_time": "2025-06-01 14:15:00",
        "start_time": "2025-06-01 15:00:00",
        "end_time": "2025-06-01 16:30:00"
    },    {
        "name": "王五",
        "id_number": "110101199203033456",
        "phone": "13700137003",
        "purpose": "项目洽谈",
        "visit_time": "2025-06-02 11:00:00",
        "start_time": "2025-06-02 13:00:00",
        "end_time": "2025-06-02 14:30:00"
    },    {
        "name": "赵六",
        "id_number": "110101199304044567",
        "phone": "13600136004",
        "purpose": "面试",
        "visit_time": "2025-06-03 13:30:00",
        "start_time": "2025-06-03 14:00:00",
        "end_time": "2025-06-03 15:00:00"
    },
    {
        "name": "孙七",
        "id_number": "110101199405055678",
        "phone": "13500135005",
        "purpose": "送货",
        "visit_time": "2025-06-03 14:15:00",
        "start_time": "2025-06-03 15:00:00",
        "end_time": "2025-06-03 16:00:00"
    },    {
        "name": "周八",
        "id_number": "110101199506066789",
        "phone": "13400134006",
        "purpose": "参观",
        "visit_time": "2025-06-04 15:00:00",
        "start_time": "2025-06-04 16:00:00",
        "end_time": "2025-06-04 17:30:00"
    },
    {
        "name": "吴九",
        "id_number": "110101199607077890",
        "phone": "13300133007",
        "purpose": "技术交流",
        "visit_time": "2025-06-04 15:45:00",
        "start_time": "2025-06-04 16:30:00",
        "end_time": "2025-06-04 18:00:00"
    },    {
        "name": "郑十",
        "id_number": "110101199708088901",
        "phone": "13200132008",
        "purpose": "培训",
        "visit_time": "2025-06-05 10:30:00",
        "start_time": "2025-06-05 11:00:00",
        "end_time": "2025-06-05 12:30:00"
    },
    {
        "name": "刘十一",
        "id_number": "110101199809099012",
        "phone": "13100131009",
        "purpose": "咨询",
        "visit_time": "2025-06-05 14:15:00",
        "start_time": "2025-06-05 14:30:00",
        "end_time": "2025-06-05 15:30:00"
    },
    {
        "name": "陈十二",
        "id_number": "110101199910100123",
        "phone": "13000130010",
        "purpose": "签约",
        "visit_time": "2025-06-05 16:00:00",
        "start_time": "2025-06-05 16:30:00",
        "end_time": "2025-06-05 17:30:00"
    },
    # 添加5条新数据
    {
        "name": "杨十三",
        "id_number": "110101199011110234",
        "phone": "13911131011",
        "purpose": "产品演示",
        "visit_time": "2025-06-06 09:00:00",
        "start_time": "2025-06-06 09:30:00",
        "end_time": "2025-06-06 11:00:00"
    },
    {
        "name": "黄十四",
        "id_number": "110101199112120345",
        "phone": "13822232012",
        "purpose": "合作洽谈",
        "visit_time": "2025-06-06 13:30:00",
        "start_time": "2025-06-06 14:00:00",
        "end_time": "2025-06-06 15:30:00"
    },
    {
        "name": "林十五",
        "id_number": "110101199213130456",
        "phone": "13733333013",
        "purpose": "设备安装",
        "visit_time": "2025-06-07 10:15:00",
        "start_time": "2025-06-07 10:30:00",
        "end_time": "2025-06-07 12:00:00"
    },
    {
        "name": "朱十六",
        "id_number": "110101199314140567",
        "phone": "13644434014",
        "purpose": "售后服务",
        "visit_time": "2025-06-07 14:45:00",
        "start_time": "2025-06-07 15:00:00",
        "end_time": "2025-06-07 16:30:00"
    },
    {
        "name": "赵十七",
        "id_number": "110101199415150678",
        "phone": "13555535015",
        "purpose": "资料收集",
        "visit_time": "2025-06-08 09:30:00",
        "start_time": "2025-06-08 10:00:00",
        "end_time": "2025-06-08 11:30:00"
    }
]

def init_sample_data():
    with app.app_context():
        db = get_db()
        try:
            for visitor in sample_visitors:
                db.execute(
                    'INSERT INTO visitors (name, id_number, phone, purpose, visit_time, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (visitor['name'], visitor['id_number'], visitor['phone'], visitor['purpose'], 
                     visitor['visit_time'], visitor['start_time'], visitor['end_time'])
                )
            db.commit()
            print("示例数据初始化成功！")
        except Exception as e:
            print(f"初始化示例数据时出错：{e}")

if __name__ == '__main__':
    init_sample_data()
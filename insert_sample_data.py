import sqlite3
import random
from datetime import datetime, timedelta

# 连接到数据库
conn = sqlite3.connect('visitor.db')
cursor = conn.cursor()

# 生成随机姓名
first_names = ["张", "王", "李", "赵", "刘", "陈", "杨", "黄", "周", "吴", "郑", "孙", "马", "朱", "胡", "林", "郭", "何", "高", "罗"]
last_names = ["伟", "芳", "娜", "秀英", "敏", "静", "强", "磊", "军", "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀兰", "霞", "平", "刚"]

# 生成随机来访目的
purposes = ["商务会议", "技术交流", "产品咨询", "售后服务", "面试", "参观", "培训", "项目合作", "私人拜访", "其他"]

# 生成随机电话号码
def generate_phone():
    prefixes = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", 
                "150", "151", "152", "153", "155", "156", "157", "158", "159", 
                "180", "181", "182", "183", "184", "185", "186", "187", "188", "189"]
    prefix = random.choice(prefixes)
    suffix = ''.join(random.choice("0123456789") for _ in range(8))
    return prefix + suffix

# 生成随机身份证号
def generate_id_number():
    # 地区码(6位) + 出生日期(8位) + 顺序码(3位) + 校验码(1位)
    area_code = random.choice(["110101", "310101", "440101", "510101", "330101"])
    
    # 生成1970-2000年之间的出生日期
    start_date = datetime(1970, 1, 1)
    end_date = datetime(2000, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    birth_date = start_date + timedelta(days=random_days)
    birth_date_str = birth_date.strftime("%Y%m%d")
    
    # 顺序码
    sequence = ''.join(random.choice("0123456789") for _ in range(3))
    
    # 校验码 (简化处理，实际上有特定算法)
    check_code = random.choice("0123456789X")
    
    return area_code + birth_date_str + sequence + check_code

# 生成随机访问时间（过去30天内）
def generate_visit_time():
    now = datetime.now()
    days_ago = random.randint(0, 30)
    hours_ago = random.randint(0, 23)
    minutes_ago = random.randint(0, 59)
    
    visit_time = now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
    return visit_time.strftime("%Y-%m-%d %H:%M:%S")

# 生成开始和结束时间（基于访问时间）
def generate_start_end_times(visit_time):
    visit_dt = datetime.strptime(visit_time, "%Y-%m-%d %H:%M:%S")
    
    # 开始时间：访问时间后的0-60分钟
    start_minutes = random.randint(0, 60)
    start_time = visit_dt + timedelta(minutes=start_minutes)
    
    # 结束时间：开始时间后的30-180分钟
    end_minutes = random.randint(30, 180)
    end_time = start_time + timedelta(minutes=end_minutes)
    
    return start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time.strftime("%Y-%m-%d %H:%M:%S")

# 插入15条样本数据
sample_data = []
for i in range(15):
    name = random.choice(first_names) + random.choice(last_names)
    id_number = generate_id_number()
    phone = generate_phone()
    purpose = random.choice(purposes)
    visit_time = generate_visit_time()
    start_time, end_time = generate_start_end_times(visit_time)
    
    sample_data.append((name, id_number, phone, purpose, visit_time, start_time, end_time))

# 执行插入
try:
    cursor.executemany(
        "INSERT INTO visitors (name, id_number, phone, purpose, visit_time, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?, ?)",
        sample_data
    )
    conn.commit()
    print(f"成功插入 {cursor.rowcount} 条访客数据")
except sqlite3.Error as e:
    print(f"插入数据时出错: {e}")
finally:
    conn.close()
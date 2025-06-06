# 访客管理系统

基于Flask的访客管理系统，支持访客登记、查询和数据统计功能。

## Docker部署说明

### 使用docker-compose部署（推荐）

1. 确保已安装Docker和docker-compose
2. 在项目根目录下运行：
```bash
docker-compose up -d
```
3. 访问 http://localhost:5000 即可使用系统

### 手动构建并运行

1. 构建Docker镜像：
```bash
docker build -t visitor-management .
```

2. 运行容器：
```bash
docker run -d -p 5000:5000 -v visitor_data:/app/data --name visitor-app visitor-management
```

## 系统功能

- 访客登记：记录访客信息，包括姓名、身份证号、电话等
- 访客查询：支持按姓名、身份证号、电话号码和时间范围查询
- 数据统计：展示今日、本周、本月的访客统计数据

## 技术栈

- Python 3.11
- Flask 3.0.0
- SQLite3
- Bootstrap 5.3.2
- Chart.js

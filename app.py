from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于flash消息
DATABASE = 'data/visitor.db'  # 将数据库文件放在data目录下

@app.template_filter('format_datetime')
def format_datetime(value):
    """Format a datetime string to a more readable format."""
    if not value:
        return ""
    try:
        dt = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y年%m月%d日 %H:%M")
    except (ValueError, TypeError):
        return value  # 如果转换失败，返回原始值

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        id_number = request.form['id_number']
        phone = request.form['phone']
        purpose = request.form['purpose']
        visit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        
        db = get_db()
        try:
            db.execute(
                'INSERT INTO visitors (name, id_number, phone, purpose, visit_time, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (name, id_number, phone, purpose, visit_time, start_time, end_time)
            )
            db.commit()
            flash('访客信息登记成功！', 'success')
        except sqlite3.Error as e:
            flash('登记失败：' + str(e), 'error')
        
        return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/search')
def search():
    visitors = []
    db = get_db()
    
    # 获取搜索参数
    search_term = request.args.get('search_term', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    
    # 构建查询
    query = '''SELECT * FROM visitors WHERE 1=1'''
    params = []
    
    if search_term:
        query += ''' AND (name LIKE ? OR id_number LIKE ? OR phone LIKE ?)'''
        search_pattern = f'%{search_term}%'
        params.extend([search_pattern] * 3)
        
    if start_date:
        query += ''' AND date(visit_time) >= date(?)'''
        params.append(start_date)
        
    if end_date:
        query += ''' AND date(visit_time) <= date(?)'''
        params.append(end_date)
    
    query += ''' ORDER BY visit_time DESC'''
    visitors = db.execute(query, params).fetchall()
    
    return render_template('search.html', visitors=visitors)

def get_visitor_stats():
    db = get_db()
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    # 获取当天访客数量（实时）
    today_count = db.execute('''
        SELECT COUNT(*) as count FROM visitors 
        WHERE date(visit_time) = date(?)
    ''', (today,)).fetchone()['count']
      # 获取本周访客数量（周一到现在，按天统计）
    week_start = (now - datetime.timedelta(days=now.weekday())).strftime("%Y-%m-%d")  # 获取本周一的日期
    week_stats = db.execute('''
        WITH RECURSIVE dates(date) AS (
            SELECT date(?) -- 本周一
            UNION ALL
            SELECT date(date, '+1 day')
            FROM dates
            WHERE date < date(?)
        )
        SELECT dates.date as date,
               COALESCE(COUNT(visitors.id), 0) as count
        FROM dates
        LEFT JOIN visitors ON date(visitors.visit_time) = dates.date
        GROUP BY dates.date
        ORDER BY dates.date
    ''', (week_start, today)).fetchall()
    
    # 获取本月访客数量（1号到现在，按天统计）
    month_stats = db.execute('''
        WITH RECURSIVE dates(date) AS (
            SELECT date(?, 'start of month') -- 本月1号
            UNION ALL
            SELECT date(date, '+1 day')
            FROM dates
            WHERE date < date(?)
        )
        SELECT dates.date as date,
               COALESCE(COUNT(visitors.id), 0) as count
        FROM dates
        LEFT JOIN visitors ON date(visitors.visit_time) = dates.date
        GROUP BY dates.date
        ORDER BY dates.date
    ''', (today, today)).fetchall()
    
    return {
        'today_count': today_count,
        'week_stats': [dict(row) for row in week_stats],
        'month_stats': [dict(row) for row in month_stats]
    }

@app.route('/analytics')
def analytics():
    stats = get_visitor_stats()
    return render_template('analytics.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True)

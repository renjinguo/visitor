from flask import Flask, render_template, request, redirect, url_for, flash, g, session
import sqlite3
import datetime
import hashlib
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于session和flash消息

# 登录验证装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 密码加密函数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'visitor.db')  # 数据库文件路径

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
    if 'user_id' in session:
        return redirect(url_for('register'))
    return redirect(url_for('login'))

# 登录尝试记录
login_attempts = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_data = {}
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        remember = 'remember' in request.form
        
        # 保存用户名以便回显
        form_data = {'username': username}
        
        # 检查登录尝试次数
        ip = request.remote_addr
        current_time = datetime.datetime.now()
        if ip in login_attempts:
            attempts = login_attempts[ip]
            # 如果距离上次尝试超过30分钟，重置尝试次数
            if (current_time - attempts['last_attempt']).seconds > 1800:
                attempts['count'] = 0
            # 如果尝试次数超过5次，且最后一次尝试在30分钟内
            elif attempts['count'] >= 5:
                remaining_time = 30 - (current_time - attempts['last_attempt']).seconds // 60
                flash(f'登录尝试次数过多，请{remaining_time}分钟后再试', 'error')
                return render_template('login.html', form_data=form_data)
        else:
            login_attempts[ip] = {'count': 0, 'last_attempt': current_time}
        
        # 输入验证
        if not username:
            flash('用户名不能为空', 'error')
        elif not password:
            flash('密码不能为空', 'error')
        else:
            db = get_db()
            user = db.execute(
                'SELECT * FROM system_users WHERE username = ?', (username,)
            ).fetchone()
            
            if user is None:
                flash('用户名不存在', 'error')
                login_attempts[ip]['count'] += 1
            elif user['password'] != hash_password(password):
                flash('密码不正确', 'error')
                login_attempts[ip]['count'] += 1
            else:
                # 登录成功，清除之前的session并设置新session
                session.clear()
                session['user_id'] = user['id']
                session['username'] = user['username']
                
                # 如果选择了"记住我"，设置session的有效期为30天
                if remember:
                    session.permanent = True
                    app.permanent_session_lifetime = datetime.timedelta(days=30)
                
                # 更新最后登录时间
                db.execute(
                    'UPDATE system_users SET last_login = ? WHERE id = ?',
                    (current_time.strftime("%Y-%m-%d %H:%M:%S"), user['id'])
                )
                db.commit()
                
                # 清除该IP的登录尝试记录
                if ip in login_attempts:
                    del login_attempts[ip]
                
                flash('登录成功！', 'success')
                return redirect(url_for('register'))
            
            login_attempts[ip]['last_attempt'] = current_time
    
    return render_template('login.html', form_data=form_data)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    form_data = {}
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # 保存表单数据以便在验证失败时回显
        form_data = {
            'username': username,
            'email': email
        }
        
        # 字段验证
        if not username:
            error = '用户名不能为空'
        elif len(username) < 3:
            error = '用户名长度不能少于3个字符'
        elif len(username) > 20:
            error = '用户名长度不能超过20个字符'
        elif not email:
            error = '邮箱不能为空'
        elif '@' not in email or '.' not in email:
            error = '请输入有效的邮箱地址'
        elif not password:
            error = '密码不能为空'
        elif len(password) < 6:
            error = '密码长度不能少于6个字符'
        elif len(password) > 20:
            error = '密码长度不能超过20个字符'
        elif not any(c.isupper() for c in password) or not any(c.islower() for c in password) or not any(c.isdigit() for c in password):
            error = '密码必须包含大小写字母和数字'
        elif password != confirm_password:
            error = '两次输入的密码不一致'
        else:
            db = get_db()
            try:
                # 检查用户名是否已存在
                if db.execute('SELECT id FROM system_users WHERE username = ?', (username,)).fetchone() is not None:
                    error = '用户名已被使用'
                # 检查邮箱是否已存在
                elif db.execute('SELECT id FROM system_users WHERE email = ?', (email,)).fetchone() is not None:
                    error = '邮箱已被注册'
                else:
                    # 创建新用户
                    db.execute(
                        'INSERT INTO system_users (username, email, password, created_at) VALUES (?, ?, ?, ?)',
                        (username, email, hash_password(password), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    )
                    db.commit()
                    flash('注册成功，请登录', 'success')
                    return redirect(url_for('login'))
            except sqlite3.Error as e:
                error = f'注册失败: {str(e)}'
        
        if error:
            flash(error, 'error')
    
    return render_template('signup.html', form_data=form_data)

@app.route('/logout')
def logout():
    session.clear()
    flash('您已成功退出登录', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
def analytics():
    stats = get_visitor_stats()
    return render_template('analytics.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True)
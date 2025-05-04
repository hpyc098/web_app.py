from flask import Flask, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 用于加密 session

# 用户数据库：用户名 -> 密码和角色
USERS = {
    'Hpyc': {'password': 'Hpyc20131121', 'role': 'admin'},
    'user1': {'password': '123456', 'role': 'user'}  # 示例普通用户
}

login_logs = []  # 登录日志


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = USERS.get(username)

        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']

            login_logs.append({
                'user': username,
                'ip': request.remote_addr,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

            return redirect(url_for('home'))
        else:
            return '''
                <h3>用户名或密码错误</h3>
                <a href="/">返回</a>
            '''
    return '''
        <h2>登录</h2>
        <form method="post">
            用户名: <input type="text" name="username"><br>
            密码: <input type="password" name="password"><br>
            <input type="submit" value="登录">
        </form>
        <a href="/register">注册账号</a> | 
        <a href="/forgot">忘记密码？</a>
    '''


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS:
            return '<h3>用户名已存在</h3><a href="/register">返回</a>'
        USERS[username] = {'password': password, 'role': 'user'}
        return '<h3>注册成功！请返回登录</h3><a href="/">去登录</a>'
    return '''
        <h2>注册</h2>
        <form method="post">
            用户名: <input type="text" name="username"><br>
            密码: <input type="password" name="password"><br>
            <input type="submit" value="注册">
        </form>
    '''


@app.route('/forgot')
def forgot():
    return '''
        <h3>暂不支持找回密码，请联系管理员。</h3>
        <a href="/">返回登录</a>
    '''


@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    role = session.get('role', 'user')

    return f'''
        <h1>欢迎 {username}！</h1>
        <p>你的身份是：<b>{role}</b></p>
        <p>使用 GitHub 编辑 + Render 部署</p>
        <a href="/logout">退出登录</a>
        <hr>
        <h3>最近登录记录：</h3>
        {"".join([f"<p>{log['time']} - {log['user']} @ {log['ip']}</p>" for log in login_logs[-5:]])}
    '''


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))




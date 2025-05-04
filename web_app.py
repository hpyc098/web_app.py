from flask import Flask, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 用户数据
USERS = {
    'Hpyc': {'password': 'Hpyc20131121', 'role': 'admin'},
    'user1': {'password': '123456', 'role': 'user'}
}

login_logs = []

BASE_STYLE = '''
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f8f9fa; color: #333; }
        h1, h2 { color: #343a40; }
        input[type=text], input[type=password] {
            padding: 8px; width: 200px; margin: 5px 0;
            border: 1px solid #ccc; border-radius: 4px;
        }
        input[type=submit] {
            padding: 8px 16px;
            background: #007bff; color: white;
            border: none; border-radius: 4px;
            cursor: pointer;
        }
        input[type=submit]:hover { background: #0056b3; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .container { max-width: 600px; margin: auto; }
    </style>
'''

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
            return BASE_STYLE + '''
                <div class="container">
                    <h3>用户名或密码错误</h3>
                    <a href="/">返回</a>
                </div>
            '''
    return BASE_STYLE + '''
        <div class="container">
            <h2>登录</h2>
            <form method="post">
                用户名: <input type="text" name="username"><br>
                密码: <input type="password" name="password"><br>
                <input type="submit" value="登录">
            </form>
            <p><a href="/register">注册账号</a> | <a href="/forgot">忘记密码？</a></p>
        </div>
    '''


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS:
            return BASE_STYLE + '<div class="container"><h3>用户名已存在</h3><a href="/register">返回</a></div>'
        USERS[username] = {'password': password, 'role': 'user'}
        return BASE_STYLE + '<div class="container"><h3>注册成功！</h3><a href="/">去登录</a></div>'
    return BASE_STYLE + '''
        <div class="container">
            <h2>注册</h2>
            <form method="post">
                用户名: <input type="text" name="username"><br>
                密码: <input type="password" name="password"><br>
                <input type="submit" value="注册">
            </form>
        </div>
    '''


@app.route('/forgot')
def forgot():
    return BASE_STYLE + '''
        <div class="container">
            <h3>暂不支持找回密码，请联系管理员。</h3>
            <a href="/">返回登录</a>
        </div>
    '''


@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    return BASE_STYLE + f'''
        <div class="container">
            <h1>欢迎Hpyc的的用户，{username}！</h1>
            <p><a href="/logout">退出登录</a></p>
            {'<p><a href="/admin">用户管理（仅管理员）</a></p>' if session.get('role') == 'admin' else ''}
        </div>
    '''


@app.route('/admin')
def admin_panel():
    if session.get('role') != 'admin':
        return BASE_STYLE + '<div class="container"><h3>没有权利</h3><a href="/">返回主页</a></div>'

    user_list_html = ''.join([f"<p>用户名：<b>{u}</b>，密码：<b>{USERS[u]['password']}</b></p>" for u in USERS])
    return BASE_STYLE + f'''
        <div class="container">
            <h2>用户管理面板</h2>
            {user_list_html}
            <p><a href="/home">返回主页</a></p>
        </div>
    '''


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

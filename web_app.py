# 文件名建议：main.py

from flask import Flask, request

app = Flask(__name__)

# 设置密码（你可以改成你想要的）
PASSWORD = 'Hpyc20131121'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_password = request.form.get('password')
        if user_password == PASSWORD:
            return '''
                <html>
                    <head><title>这个名字奇怪吧</title></head>
                    <body>
                        <h1>欢迎！</h1>
                        
                        <h1>使用github进行编辑使用Render Web</h1>
                        <p>cpu.0.1</p>
                    </body>
                </html>
            '''
        else:
            return '''
                <h3>密码错误，请重新输入</h3>
                <a href="/">返回</a>
            '''
    return '''
        <form method="post">
            <h2>请输入密码进入页面：</h2>
            <input type="password" name="password">
            <input type="submit" value="登录">
        </form>
    '''

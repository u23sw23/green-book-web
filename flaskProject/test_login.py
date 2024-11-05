from flask import Flask, request, render_template, flash, url_for, redirect, session
import pymysql
def get_db_connection():
    conn = pymysql.connect(
        host='127.0.0.1',
        database='test',
        port=3306
    )
    return conn
app = Flask(__name__)
app.secret_key = '985915'
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute('INSERT INTO test.login_test (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
                conn.commit()
                return render_template('log_in_page.html')
            except Exception as e:
                flash('登录失败：' + str(e))
            finally:
                cur.close()
                conn.close()
            return render_template('log_in_page.html') #原先登陆界面，上面都是
        else:
            username = request.form['username'] #这行代码从请求的表单数据中获取 name="username"的值，并将其赋值给变量 username
            password = request.form['password'] #request.form 是一个类似字典的对象，包含了所有的表单数据
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute('SELECT * FROM test.login_test WHERE username = %s AND password = %s', (username, password))
                result = cur.fetchone() #是一个游标（cursor）对象的方法，用于从结果集中获取第一条记录
                print(username + password)  # 打印用户名和密码到控制台（也就是这里）
                if result:
                    return render_template('home.html') #跳转到主页
                else:
                    flash('Username or password is incorrect!')
            except Exception as e:
                flash('登录出现问题：' + str(e))
            finally:
                cur.close()
                conn.close()
            return render_template('log_in_page.html') # 重新渲染登录页面
    else:
        return render_template('log_in_page.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/login')
def login1():
    return render_template('log_in_page.html')

@app.route('/home')
def home1():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

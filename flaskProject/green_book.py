from flask import Flask, request, render_template, flash, url_for, redirect, session
import pymysql  #确保：1.服务里数据库都启动 2.表已经选择了框架
def get_db_connection():
    conn = pymysql.connect(
        host='127.0.0.1',
        database='test',
        port=3306
    )
    return conn

def get_posts(introduction_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)#使用 DictCursor 会让查询结果以字典（dictionary）形式返回，而不是默认的元组（tuple）形式
    sql = f"SELECT * FROM test.{introduction_id} ORDER BY timestamp DESC"
    cursor.execute(sql)
    posts = cursor.fetchall()#获取当前查询结果中的所有行，返回一个列表，列表中的每一项都是一行数据
    cursor.close()
    conn.close()
    return posts
app = Flask(__name__)
app.secret_key = '985915'
introduction_data = {
    'stay_mierica': {
        'name': 'Stay Mierica',
        'image_url': '../static/public/hotel1.jpg',
        'description': '这是Stay Mierica餐厅的详细介绍...'
    },
    'easy_join_coffee': {
        'name': '另一家餐厅',
        'image_url': '../static/public/coffee1.jpg',
        'description': '这是另一家餐厅的详细介绍...'
    },
    'puppy_coffee': {
        'name': '另一家餐厅',
        'image_url': '../static/public/coffee2.jpg',
        'description': '这是另一家餐厅的详细介绍...'
    },
    'freedom_coffee': {
        'name': '另一家餐厅',
        'image_url': '../static/public/coffee3.jpg',
        'description': '这是另一家餐厅的详细介绍...'
    },
    'Pets_Corner': {
        'name': '另一家餐厅',
        'image_url': '../static/public/shop1.jpg',
        'description': '这是另一家餐厅的详细介绍...'
    },
    'Petco': {
        'name': '另一家餐厅',
        'image_url': '../static/public/shop2.jpg',
        'description': '这是另一家餐厅的详细介绍...'
    }
}

@app.route('/introduction/<introduction_id>', methods=['GET', 'POST'])
def introduction_detail(introduction_id):
    # 获取场所信息
    place_info = introduction_data.get(introduction_id)
    if not place_info:
        flash('未找到该场所信息')
        return redirect(url_for('home'))
    # 获取评论列表
    try:
        posts = get_posts(introduction_id)
    except Exception as e:
        posts = []
        flash(f'获取评论失败：{str(e)}')

    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = f"INSERT INTO test.{introduction_id} (username, content, timestamp) VALUES (%s, %s, NOW())"
            cursor.execute(sql, (username, content))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('introduction_detail', introduction_id=introduction_id))#将当前的 introduction_id 值作为参数传递给路由，告诉Flask要重新定向到哪个页面
        except Exception as e:
            flash(f'提交评论失败：{str(e)}')

    # GET 请求时渲染模板
    return render_template('introduction_detail.html',  
                           introduction=place_info,  # 改为与模板中使用的变量名一致
                           posts=posts,
                           introduction_id=introduction_id)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            conn = None
            cur = None
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
            conn = None
            cur = None
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute('SELECT * FROM test.login_test WHERE username = %s AND password = %s', (username, password))
                result = cur.fetchone() #是一个游标（cursor）对象的方法，用于从结果集中获取第一条记录
                print(f"用户名为{username}密码为{password}的用户刚刚登陆了网站")  # 打印用户名和密码到控制台（也就是这里）
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
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)

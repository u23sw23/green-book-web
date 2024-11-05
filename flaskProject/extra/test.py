from flask import Flask, request, render_template, redirect, url_for
import pymysql

app = Flask(__name__)
def get_db_connection():
    connection = pymysql.connect(
        host='127.0.0.1',
        database='test',
        port=3306,   #这里不能带上password这些，加了就判错
    )
    return connection
@app.route('/post', methods=['GET', 'POST'])#@app.route是一个装饰器，用于告诉Flask什么样的URL能触发我们的函数
def post():
    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO posts (username, content, timestamp) VALUES (%s, %s, NOW())', (username, content))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))  # url_for('index') 将返回函数index()所在的路径即/
    else:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM posts ORDER BY timestamp DESC')
        posts = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('test.html', posts=posts)
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM posts ORDER BY timestamp DESC')
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('test.html', posts=posts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
from flask import Flask, request, render_template, flash
import pymysql

def get_db_connection(): #包裹在函数里，只有在登录的时候才使用数据库的连接
    conn = pymysql.connect( #你的 mysql有点问题，现在是无密码模式，去看看
        host='127.0.0.1',
        database='test',
        port=3306
    )
    return conn
app = Flask(__name__)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO test.login_test (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
            return render_template('extra/登陆界面.html')
        except Exception as e:
            flash('登录失败：' + str(e))
        finally:
            cursor.close()
            conn.close()
        return render_template('extra/登陆界面.html')
    else:
        return render_template('extra/注册界面.html')
if __name__ == '__main__':
    app.run(debug=True, port=5000)


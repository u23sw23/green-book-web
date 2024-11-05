from flask import Flask, request, render_template, redirect, url_for
import pymysql

app = Flask(__name__)

def get_db_connection():
    connection = pymysql.connect(
        host='127.0.0.1',
        database='test',
        port=3306,
        # Ensure password is securely managed
    )
    return connection

def get_posts():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM posts ORDER BY timestamp DESC')
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return posts

@app.route('/', methods=['GET', 'POST'])
def index():
    posts = get_posts()
    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO posts (username, content, timestamp) VALUES (%s, %s, NOW())', (username, content))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('test.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

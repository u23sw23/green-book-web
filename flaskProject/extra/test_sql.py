import pymysql

conn=pymysql.connect(  #你的 mysql有点问题，现在是无密码模式，去看看
    host='127.0.0.1',
    database='test',
    port=3306
)

cursor=conn.cursor() #创建一个游标对象 cursor，用于执行 SQL 语句并获取结果。
cursor.execute('insert into login_test ( `username`, `password`) values ( "d", "D");') #注意了，列名要用反引号，字符串要用双引号（不能单引号！）
cursor.execute('DELETE FROM login_test WHERE `username`="d";')
cursor.execute('select * from login_test') #这里面就直接写sql查询语句了
result=cursor.fetchall()
print(f'查询到的结果是：{result}')

cursor.close()
conn.close()
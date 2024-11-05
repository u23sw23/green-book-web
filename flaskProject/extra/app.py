from flask import Flask,request,render_template         #flask一般用5000端口
app = Flask(__name__) #使用flsak类创建一个app对象 __name__：代表当前app.py这个模块

#常说的渲染的意思：将数据转化为可视化的结果的过程
if __name__ == '__main__':#如果当前模块作为主路由运行，就执行下面的代码
    app.run(debug=True)

#创建一个路由和视图函数的映射
@app.route('/index/<username>')  #斜杠代表跟路由  一个装饰器，当访问这个路由的时候就使用这个装饰器，执行里面的函数
def hello_world(username):  # put application's code here
    return render_template("index.html", username=username)  #直接把index.html渲染上来

'''@app.route('/')
def test():
    user=User('admin','123456')
    return render_template('second.html',user=user)'''

@app.route('/book')  #通过？符号后接对变量的赋值来改变页面内容
def book():
    a=request.args.get('a',default=1,type=int)  #default是默认值
    return f"你来到了第{a}页！"  #访问http://127.0.0.1:5000/book?a=3，输出来到了第三页


@app.route('/login/<name>')  #带参数的url
def login(name):
    return 'Hello ' + name

#debug模式：1.随时修改，不用每次重启，但还是要保存+刷新 2.可以看到出错信息

#修改host:让别人的电脑可以访问我的网站
#修改端口号  在第五节课，这里不写

class User:
    def __init__(self,name,password):
        self.name = name
        self.password = password

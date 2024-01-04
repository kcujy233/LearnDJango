from flask import  Flask, render_template,request

app = Flask(__name__)
# 创建了网址/show/info和函数index的关系，若访问该网址则自动执行index函数
@app.route("/show/info")
def index():
    # return '中国联通'
    # 默认会去'./templates/'文件夹中找html文件
    return render_template('index.html')
@app.route("/register")
def register():
    return render_template('register.html')
@app.route("/user/list")
def user_list():
    return render_template('user_list.html')
@app.route("/reg", methods=['GET', 'POST'])
def reg():
    # 1.接收数据
    if request.method == 'GET':
        print(request.args)
    elif request.method == 'POST':
        print(request.form)
        user = request.form.get("account")
        pwd = request.form.get("passwrd")
        # hobby_list = request.form.getlist("hobby")
        # 获取单独数据使用get，获取一个标签对应多个数据返回列表使用getlist
    # 可以将数据写入到数据库中实现注册
    # 2.返回结果
    return '注册成功'

if __name__ == '__main__':
    app.run()
    # app.run(host='', port=8000)
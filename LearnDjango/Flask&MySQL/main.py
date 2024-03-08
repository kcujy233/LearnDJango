from flask import Flask,render_template,request
import pymysql
app = Flask(__name__)
@app.route("/add/user", methods = ['GET', 'POST'])
def add_user():# 从页面得到数据并插入数据库中
    if request.method == 'GET':
        return render_template("add_user.html")# 按 Ctrl+F8 切换断点。
    print(request.form)
    username = request.form.get("user")
    pwd = request.form.get("pwd")
    realname = request.form.get("real_name")
    mobile = request.form.get("mobile")
    # 链接MySQL
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset='utf8', db='unicom')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 添加数据
    sql = "insert into admin(username,passwd,real_name, mobile) values(%s,%s,%s,%s)"# 需要注意的是这个‘%s’是pysql的内部占位符，不能使用python自带的占位符
    cursor.execute(sql,[username,pwd,realname,mobile])
    conn.commit()# 提交命令
    # 关闭连接
    cursor.close()
    conn.close()
    return "添加成功"
@app.route("/show/user")
def show_user():
    # 链接MySQL
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset='utf8', db='unicom')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 添加数据
    sql = "select * from admin"# 需要注意的是这个‘%s’是pysql的内部占位符，不能使用python自带的占位符
    cursor.execute(sql)
    data_list = cursor.fetchall()# 获取数据库返还的结果
    print(data_list)
    # 关闭连接
    cursor.close()
    conn.close()
    return render_template("show_user.html", data_list=data_list)

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app.run()



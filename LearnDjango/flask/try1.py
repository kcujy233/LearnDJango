from flask import  Flask, render_template

app = Flask(__name__)
# 创建了网址/show/info和函数index的关系，若访问该网址则自动执行index函数
@app.route("/show/info")
def index():
    # return '中国联通'
    # 默认会去'./templates/'文件夹中找html文件
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
    # app.run(host='', port=8000)
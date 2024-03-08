import pymysql
# 创建链接，需要输入用户名，密码，编码，还有对应的数据库名称
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset='utf8',db='unicom')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)# 构建对象用来接受和发送数据
# 发送指令
'''增加内容：不能用字符串格式化做SQL的拼接，会有安全隐患，造成SQL注入。可以使用pysql内部函数execute来执行'''
# 方法1
# cursor.execute("insert into admin(username,passwd,mobile) values('shy','123','18894554188')")
# 方法2
# sql = "insert into admin(username,passwd,mobile) values(%s,%s,%s)"# 需要注意的是这个‘%s’是pysql的内部占位符，不能使用python自带的占位符
# cursor.execute(sql,['lxt','321','18213692576'])
# 方法3
# sql = "insert into admin(username,passwd,mobile) values(%(n1)s,%(n2)s,%(n3)s)"# 将对应占位命名，可以传递字典
# cursor.execute(sql,{"n1":'kkk',"n2":'222',"n3":'12345678910'})
# conn.commit()# 提交命令
'''查询内容'''
# sql = "select * from admin where id >= 2"
# cursor.execute(sql)
# data_list = cursor.fetchall()# 获取数据库返还的结果
# print(data_list)
'''删除数据'''
# sql = "delete from admin where id=%s"# 需要注意的是这个‘%s’是pysql的内部占位符，不能使用python自带的占位符
# cursor.execute(sql,3)
# conn.commit()# 提交命令
'''修改数据'''
sql = "update admin set passwd=%s where id=%s"# 需要注意的是这个‘%s’是pysql的内部占位符，不能使用python自带的占位符
cursor.execute(sql,['kcujy',2])
conn.commit()# 提交命令
'''增加、删除、修改的时候需要进行conn.commit()，用来提交数据'''
# 关闭连接
cursor.close()
conn.close()



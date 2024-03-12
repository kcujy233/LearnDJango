from django.db import models

# Create your models here.
'''员工管理系统'''
class Department(models.Model):
    '''部门表格'''
    # id = models.BigIntegerField(verbose_name='ID', primary_key=True)
    title = models.CharField(verbose_name='部门标题', max_length=32)
    def __str__(self):
        show = str(self.id) + self.title
        return show

class UserInfo(models.Model):
    '''员工表'''
    name = models.CharField(verbose_name='姓名', max_length=16)
    passwd = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    salary = models.DecimalField(verbose_name='账户余额',
                                 max_digits=10, decimal_places=2,
                                 default=0)# 最大位数10，小数2位，默认账户余额为0
    create_time = models.DateTimeField(verbose_name='入职时间')
    # 建立某个员工对应的部门
    # 1. 存ID？存名称？
    # 根据数据库理论知识，应该存储ID，节省存储开销
#     大公司存储名称，某一张表可能被查询的次数特别多，需要联表，联表操作比较耗时，允许数据冗余
#     2. 部门ID需不需要约束？
#     只能是数据表中已经存在的ID，在数据库中进行约束，即表对表的约束
#     departID = models.ForeignKey(to='Department', to_field='id')
#     表示关联，to表示与哪一类关联，to_fields表示与其中的哪一列关联
# ****使用DJango该方法创建关联时，出些的数据列名称自动增加”_id“也就是”departID_id“
#     3. 如果关联的部门被删除，关联的用户怎么办？
#     -- 删除用户，级联删除
    departID = models.ForeignKey(to='Department', to_field='id',
                                 on_delete=models.CASCADE)
#     -- 不删除用户，置空
#     departID = models.ForeignKey(to='Department', to_fields='id',
#                                  null=True, blank=True,
#                                  on_delete=models.SET_NULL)
#     在DJango中进行约束，即元组对表的约束，在选择性别的时候只能写1或者2
    gender_choices=(
        (1, "male"),
        (2, "female"),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)



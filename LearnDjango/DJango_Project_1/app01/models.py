from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField()
    # size = models.IntegerField(default=2)
    # data = models.IntegerField(null=True, blank=True)
    '''
    create table app01_userinfo(
        id bigint auto_increment primary key,
        name varchar(32),
        password varchar(64),
        age int
        )
    '''

from django.shortcuts import render, HttpResponse, redirect
import requests
from app01.models import UserInfo

# Create your views here.
def index(request):
    return HttpResponse("欢迎使用")

def user_list(request):
    return render(request, "user_list.html")

def news(request):
    UserInfo.objects.create(name='shy', password='123', age=24)
    return HttpResponse("返回内容")

def user_infolist(request):
#     1. 获取数据库中所有用户信息
    data_list = UserInfo.objects.all()
    # print(data_list)
    return render(request, "user_infolist.html", {"data_list":data_list})

def add_user(request):
    if request.method=="GET":
        return render(request, "add_user.html")
    usr_info = request.POST.get("user")
    pwd_info = request.POST.get("pwd")
    age_info = request.POST.get("age")
    UserInfo.objects.create(name=usr_info, password=pwd_info, age=age_info)
    # return redirect("http://127.0.0.1:8000/user/infolist")
    return redirect("/user/infolist")

def delete_user(request):
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id=nid).delete()
    # return redirect("http://128.0.0.1:8000/user/infolist")
    return redirect("/user/infolist")
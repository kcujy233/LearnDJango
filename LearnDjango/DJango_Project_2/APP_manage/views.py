from django.shortcuts import render, redirect
from APP_manage import models


# Create your views here.
def user_list(request):
    '''用户管理'''
    user_info = models.UserInfo.objects.all()
    for obj in user_info:
        name = obj.name
        age = obj.age
        pwd = obj.passwd
        salary = obj.salary
        #     获取时间的字符串
        create_time = obj.create_time.strftime("%Y-%m-%d")
        #     获取性别，即元组对应的转换
        gender = obj.get_gender_display()
        #     获取部门，即数据表对应的转换
        #     depart_id = models.Department.objects.filter(id=obj.departID_id).first().title
        depart_id = obj.departID.title

    return render(request, "user_list.html", {"user_info": user_info})


def user_add(request):
    '''添加用户'''
    if request.method == "GET":
        context = {
            "depart_list": models.Department.objects.all()
        }
        return render(request, "user_add.html", context)
    name = request.POST.get("name")
    passwd = request.POST.get("passwd")
    age = request.POST.get("age")
    salary = request.POST.get("salary")
    create_time = request.POST.get("create_time")
    gender = request.POST.get("gender")
    departID = request.POST.get("departID")
    models.UserInfo.objects.create(name=name, passwd=passwd, age=age, salary=salary, create_time=create_time,
                                   gender=gender, departID_id=departID)
    return redirect("/user/list/")


from django import forms
class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "passwd", "age", "salary", "create_time", "gender", "departID"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "passwd": forms.PasswordInput(attrs={"class": "form-control"})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            print(name, field)
            field.widget.attrs = {"class": "form-control",
                                  "placeholder":field.label}
def user_add_modelform(request):
    '''添加用户，基于ModelForm'''
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_add_modelform.html", {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect("/user/list/")
    # 校验失败
    return render(request, "user_add_modelform.html", {"form": form})




def depart_list(request):
    '''部门管理'''
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {"queryset": queryset})

def depart_add(request):
    '''添加页面'''
    if request.method == "GET":
        return render(request, 'depart_add.html')
    title = request.POST.get("title")
    models.Department.objects.create(title=title)
    return redirect("/depart/list/")

def depart_delete(request):
    '''删除部门'''
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")

def depart_edit(request, nid):
    '''修改部门'''
    if request.method == 'GET':
        total_info = models.Department.objects.filter(id=nid).first()
        title = total_info.title
        return render(request, "depart_edit.html", {"title": title})
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")

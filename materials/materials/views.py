from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


# Create your views here.
# 登录
def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    # msg="登录成功"
                    request.session['status'] = True
                    request.session['uname'] = username
                    request.session.set_expiry(300)

                return redirect("/index/")
            else:
                msg = "用户名密码错误"
        else:
            msg = "用户名不存在"
    return render(request, "templates/login.html", locals())


# 注册
def regView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if User.objects.filter(username=username):
            msg = "用户名已存在"
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            msg = "注册成功"
            return redirect("/login/")
    return render(request, "templates/register.html", locals())


# 主页
def index(request):
    return render(request, "templates/index.html", {"name": request.session.get('uname')})


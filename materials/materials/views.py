from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


# Create your views here.
# 登录
@login_required
def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    # msg="登录成功"
                    request.session['status'] = True
                    request.session['uname'] = username
                    request.session.set_expiry(300)

                return redirect("/index/")
            else:
                msg = "用户名密码错误"
        else:
            msg = "用户名不存在"
    return render(request, "login.html", locals())


# 注册
@login_required
def regView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if User.objects.filter(username=username):
            msg = "用户名已存在"
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            msg = "注册成功"
            if user:
                auth.login(request, user)
                return redirect("/login/")
    return render(request, "register.html", locals())


@login_required
def logoutPage(request):
    auth.logout(request)
    return redirect('login')  # 退出后，页面跳转至登录界面


# 主页
@login_required
def indexPage(request):
    name = request.user.username
    if name:
        result_list = Course.objects.filter(comment__user__username=name)
    return render(request, "index.html", {'user': request.user, 'name': name, 'result_list': result_list})

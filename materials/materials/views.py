from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .models import *
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
        result_list = models.Materials.objects.filter(user=request.user)
    return render(request, "index.html", {'user': request.user, 'name': name, 'result_list': result_list})


@login_required
def searchPage(request):
    # 搜索页面函数
    return render(request, 'SearchPage.html')


@login_required
@require_http_methods(['POST'])
def materialsComment(request):
    # 提交商品用函数
    user = request.user
    materials_name = request.POST.get("materials_name")
    materials_int = eval(request.POST.get("materials_int"))  # 物资数量
    materials_type = request.POST.get("materials_type")  # 物资类型
    if materials_int >= 0:
        materials = models.Materials.objects.create(
            user=user, materials_name=materials_name, materials_type=materials_type)
        materials.save()
        return redirect('index')
    else:
        raise Http404()


@login_required
@require_http_methods(['POST'])
def requestsComment(request, materials):
    # 提交商品用函数
    user = request.user
    materials_req_time = request.POST.get("materials_req_time")
    materials_req_int = eval(request.POST.get("materials_req_int"))
    materials_text = request.POST.get("materials_text")
    if materials_req_int >= 0:
        request = models.Requests.objects.create(
            user=user, materials=materials, materials_req_time=materials_req_time, materials_req_int=materials_req_int,
            materials_text=materials_text)
        request.save()
        return redirect('index')
    else:
        raise Http404()

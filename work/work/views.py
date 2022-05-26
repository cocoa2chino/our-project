from django.shortcuts import render
from . import models
import uuid

from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse

import datetime

# Create your views here.
from .models import *
from .views_constant import *


def register(request):
    if request.method == 'GET':
        data = {
            'title': '注册',
            'status': HTTP_OK,
        }
        return render(request, 'register.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword=password
        icon = request.FILES.get('icon')
        QQ = request.POST.get('QQ')
        wechat = request.POST.get('wechat')
        tel = request.POST.get('tel')
        other = request.POST.get('other')
        user = User()
        user.username = username
        user.email = email
        user.password = password
        user.repassword=password
        user.icon = icon
        user.qq = QQ
        user.wechat = wechat
        try:
            if tel:
                user.tel=int(eval(tel))
        except:
            pass
        user.other = other

        try:
            user.save()
            u_token = str(user.id)
            #send_email_activate(username, email, u_token)
        except:
            data = {
                'title': '注册',
                'status': HTTP_WRONG_EMALL,
            }
            return render(request, 'register.html', context=data)
        return redirect(reverse('login'))


def login(request):
    if request.method == 'GET':
        data = {
            'title': '登录',
        }
        return render(request, 'user/login.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.filter(username=username)
        if users.exists():
            users = users.filter(password=password)
            if users.exists():
                user = users.first()
                request.session['user_id'] = user.id
                return redirect(reverse('App:mine'))
            else:
                print('密码错误')
                return redirect('App:login')
        print('用户名不存在')
        return redirect(reverse('App:login'))

def mine(request):
    user_id = request.session.get('user_id')
    data = {
        'title': '个人主页',
        'is_login': 0,
        'is_activate': 0,
    }
    if user_id:
        user = User.objects.get(pk=user_id)
        data['is_login'] = 1
        data['user'] = user
        if user.is_active:
            data['is_activate'] = 1
        if user.icon:
            data['icon'] = '/static/uploads/' + user.icon.url
        if user_id:
            return render(request, 'main/mine.html', context=data)
        else:
            return render(request, 'main/mine_not_activated.html', context=data)
    return render(request, 'main/mine_not_login.html', context=data)

def checkuser(request):
    username = request.GET.get('username')
    users = User.objects.filter(username=username)
    data = {
        'status': HTTP_OK,
        'msg': 'username available'
    }
    if users.exists():
        data['status'] = HTTP_USER_EXISTS
        data['msg'] = 'username already exists'
    else:
        pass
    return JsonResponse(data=data)


def checkemail(request):
    email = request.GET.get('email')
    emails = User.objects.filter(email=email)
    data = {
        'status': HTTP_OK,
        'msg': 'email available'
    }
    if emails.exists():
        data['status'] = HTTP_EMAIL_EXISTS
        data['msg'] = 'email already exists'
    else:
        pass
    return JsonResponse(data=data)


def checklogin(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    users = User.objects.filter(username=username)
    data = {
        'status': HTTP_OK,
        'msg': 'user available'
    }
    if users.exists():
        users = users.filter(password=password)
        if users.exists():
            pass
        else:
            data['status'] = HTTP_WRONG_PASSWORD
            data['msg'] = 'wrong password'
    else:
        data['status'] = HTTP_USERNAME_NOT_EXISTS
        data['msg'] = 'username does not exist'
    print(data)
    return JsonResponse(data=data)






def logout(request):
    request.session.flush()
    return redirect(reverse('login'))


def modifyuser(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    is_activate = 0
    if user.is_active:
        is_activate = 1
    if request.method == 'GET':
        data = {
            'title': '修改个人信息',
            'is_login': 1,
            'is_activate': is_activate,
            'user': user,
        }
        return render(request, 'modifyuser.html', context=data)
    elif request.method == 'POST':

        username = request.POST.get('username')
        if username:
            user.username = username
        email = request.POST.get('email')
        if email:
            user.email = email
            user.is_active = 0
            if user.rank >= 1:
                user.rank -= 1
            u_token = str(user.id)
            #send_email_activate(username, email, u_token)
        password = request.POST.get('password')
        if password:
            user.password = password
        try:
            icon = request.FILES.get('icon')
            if icon:
                user.icon = icon
        except:
            pass

        qq = request.POST.get('QQ')
        if qq:
            user.qq = qq

        wechat = request.POST.get('wechat')
        if wechat:
            user.wechat = wechat

        tel = request.POST.get('tel')
        if tel:
            user.tel = tel

        other = request.POST.get('other')
        if other:
            user.other = other

        user.save()
        return redirect(reverse('mine'))



def index(request):
    return render(request, 'index.html')


def entry_storage(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        entry_id = request.GET.getlist('entry_id')
        goods_id = request.GET.getlist('goods_id')
        storage_id = request.GET.getlist('storage_id')
        supplier_id = request.GET.getlist('supplier_id')
        goods_price = request.GET.getlist('goods_price')
        goods_num = request.GET.getlist('goods_num')
        entry_data = request.GET.getlist('entry_data')
        insert = models.entry_bill.objects.create(entry_id=entry_id[0], goods_id=goods_id[0], storage_id=storage_id[0],
                                                  supplier_id=supplier_id[0], goods_price=goods_price[0],
                                                  goods_num=goods_num[0], entry_data=entry_data[0])
        insert.save()
    entry_bill = models.entry_bill.objects.values()
    return render(request, 'entry_storage.html', {'entry_bill': entry_bill})


def entry_storage_delete(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        entry_id = request.GET.getlist('entry_id')
        deletesql = models.entry_bill.objects.filter(entry_id=entry_id[0]).delete()
    entry_bill = models.entry_bill.objects.values()
    return render(request, 'entry_storage.html', {'entry_bill': entry_bill})


def goods(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        goods_id = request.GET.getlist('goods_id')
        goods_name = request.GET.getlist('goods_name')
        goods_num = request.GET.getlist('goods_num')
        goods_sort = request.GET.getlist('goods_sort')
        goods_remark = request.GET.getlist('goods_remark')
        insert = models.goods.objects.create(goods_id=goods_id[0], goods_name=goods_name[0], goods_num=goods_num[0],
                                             goods_sort=goods_sort[0], goods_remark=goods_remark[0])
        insert.save()
    goods = models.goods.objects.values()
    return render(request, 'goods.html', {'goods': goods})


def goods_delete(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        goods_id = request.GET.getlist('goods_id')
        deletesql = models.goods.objects.filter(goods_id=goods_id[0]).delete()
    goods = models.goods.objects.values()

    return render(request, 'goods.html', {'goods': goods})


def out_storage(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        out_id = request.GET.getlist('out_id')
        goods_id = request.GET.getlist('goods_id')
        storage_id = request.GET.getlist('storage_id')
        subscriber_id = request.GET.getlist('subscriber_id')
        goods_price = request.GET.getlist('goods_price')
        goods_num = request.GET.getlist('goods_num')
        out_data = request.GET.getlist('out_data')
        insert = models.out_bill.objects.create(out_id=out_id[0], goods_id=goods_id[0], storage_id=storage_id[0],
                                                subscriber_id=subscriber_id[0], goods_price=goods_price[0],
                                                goods_num=goods_num[0], out_data=out_data[0])
        insert.save()
    out_bill = models.out_bill.objects.values()
    return render(request, 'out_storage.html', {'out_bill': out_bill})


def out_storage_delete(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        out_id = request.GET.getlist('out_id')
        deletesql = models.out_bill.objects.filter(out_id=out_id[0]).delete()
    out_bill = models.out_bill.objects.values()

    return render(request, 'out_storage.html', {'out_bill': out_bill})


def storage(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        storage_id = request.GET.getlist('storage_id')
        storage_name = request.GET.getlist('storage_name')

        insert = models.storage.objects.create(storage_id=storage_id[0], storage_name=storage_name[0])
        insert.save()
    storage = models.storage.objects.values()
    return render(request, 'storage.html', {'storage': storage})


def storage_delete(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        storage_id = request.GET.getlist('storage_id')
        deletesql = models.v.objects.filter(storage_id=storage_id[0]).delete()
    storage = models.storage.objects.values()

    return render(request, 'storage.html', {'subscriber': storage})


def subscriber(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        subscriber_id = request.GET.getlist('subscriber_id')
        subscriber_name = request.GET.getlist('subscriber_name')

        insert = models.subscriber.objects.create(subscriber_id=subscriber_id[0], subscriber_name=subscriber_name[0])
        insert.save()
    subscriber = models.subscriber.objects.values()
    return render(request, 'subscriber.html', {'subscriber': subscriber})


def subscriber_delete(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        subscriber_id = request.GET.getlist('subscriber_id')
        deletesql = models.subscriber.objects.filter(subscriber_id=subscriber_id[0]).delete()
    subscriber = models.subscriber.objects.values()

    return render(request, 'subscriber.html', {'subscriber': subscriber})


def supplier(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        supplier_id = request.GET.getlist('supplier_id')
        supplier_name = request.GET.getlist('supplier_name')

        insert = models.supplier.objects.create(supplier_id=supplier_id[0], supplier_name=supplier_name[0])
        insert.save()
    supplier = models.supplier.objects.values()
    return render(request, 'supplier.html', {'supplier': supplier})


def supplier_delete(request):
    if request.is_ajax():
        # 获取其中的某个键的值
        supplier_id = request.GET.getlist('supplier_id')
        deletesql = models.supplier.objects.filter(supplier_id=supplier_id[0]).delete()
    supplier = models.supplier.objects.values()

    return render(request, 'supplier.html', {'supplier': supplier})
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout, authenticate
from .models import *
from django.urls import reverse
import random
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta
from django.core.paginator import Paginator


# Create your views here.
# 登录
def get_ticket():
    ticket = ''
    s = 'abcdefghijklmnopqrstuvwxyz1234567890'
    for x in range(100):
        ticket += random.choice(s)
    return ticket


# 后台登陆
def admin_login(request):
    if request.method == 'GET':
        return render(request, 'admin/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = {}
        # 验证信息是否填写完整
        if not all([username, password]):
            data['msg'] = '用户名或者密码不能为空'
        # 验证用户是否注册
        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            # 验证密码是否正确
            if check_password(password, user.password):
                # 如果密码正确将ticket值保存在cookie中
                ticket = get_ticket()
                response = HttpResponseRedirect(reverse('admin_index'))
                out_time = datetime.now() + timedelta(days=1)
                response.set_cookie('ticket', ticket, expires=out_time)
                # 保存ticket值到数据库user_ticket表中
                UserTicketModel.objects.create(user=user,
                                               out_time=out_time,
                                               ticket=ticket)

                return response
            else:
                msg = '用户名或密码错误'
                return render(request, 'login.html', {'msg': msg})
        else:
            msg = '用户名不存在,请注册后在登陆'
            return render(request, 'login.html', {'msg': msg})


# 后台首页
def admin_index(request):
    kind=ArticleCategory.objects.create(kind="食品")
    kind.save()
    if request.method == 'GET':
        return render(request, 'admin/index.html')


# 商品列表分页展示
def admin_product_list(request):
    if request.method == 'GET':
        num = request.GET.get('page_num', 1)
        goods = GoodsValue.objects.filter(isDelete=0)
        paginator = Paginator(goods, 5)
        pages = paginator.page(num)
        data = {
            'goods': pages
        }
        return render(request, 'admin/product_list.html', data)


# 添加商品
def admin_product_detail(request):
    if request.method == 'GET':
        kinds = ArticleCategory.objects.all()
        data = {
            'kinds': kinds
        }
        return render(request, 'admin/product_detail.html', data)

    if request.method == 'POST':
        g_name = request.POST.get('g_name')
        g_img = request.FILES.get('g_img')
        g_num = request.POST.get('g_num')
        g_price = request.POST.get('g_price')
        g_unit = request.POST.get('g_unit')
        g_repertory = request.POST.get('g_repertory')
        kind = request.POST.get('kind')
        gtype_id = ArticleCategory.objects.filter(kind=kind).first().id

        if not all([g_name, g_img, g_num, g_price, g_unit, g_repertory, gtype_id]):
            data = {
                'msg': '商品信息请填写完整'
            }
            return render(request, 'admin/product_detail.html', data)
        # 添加商品到数据库sx_goods表中
        GoodsValue.objects.create(g_name=g_name,
                                  g_img=g_img,
                                  g_num=g_num,
                                  g_price=g_price,
                                  g_unit=g_unit,
                                  g_repertory=g_repertory,
                                  gtype_id=gtype_id
                                  )
        # 商品添加成功后跳转到商品列表页
        return HttpResponseRedirect(reverse('admin_product_list'))


# 修改商品
def admin_change_goods(request):
    if request.method == 'GET':
        kinds = ArticleCategory.objects.all()
        g_id = request.GET.get('g_id')
        goods = GoodsValue.objects.filter(id=g_id).first()
        data = {
            'kinds': kinds,
            'goods': goods
        }
        return render(request, 'admin/product_detail.html', data)

    if request.method == 'POST':
        g_name = request.POST.get('g_name')
        g_img = request.FILES.get('g_img')
        g_num = request.POST.get('g_num')
        g_price = request.POST.get('g_price')
        g_unit = request.POST.get('g_unit')
        g_repertory = request.POST.get('g_repertory')
        kind = request.POST.get('kind')
        gtype_id = ArticleCategory.objects.filter(kind=kind).first().id

        g_id = request.POST.get('g_id')
        goods = GoodsValue.objects.filter(id=g_id).first()
        data = {
            'msg': '商品修改成功'
        }
        # 如果没修改商品图片
        if not g_img:
            goods.g_name = g_name
            goods.g_num = g_num
            goods.g_price = g_price
            goods.g_unit = g_unit
            goods.g_repertory = g_repertory
            goods.gtype_id = gtype_id
            goods.save()
            return HttpResponseRedirect(reverse('admin_product_list'), data)
        # 修改商品图片
        else:
            goods.g_name = g_name
            goods.g_img = g_img
            goods.g_num = g_num
            goods.g_price = g_price
            goods.g_unit = g_unit
            goods.g_repertory = g_repertory
            goods.gtype_id = gtype_id
            goods.save()
            return HttpResponseRedirect(reverse('admin_product_list'), data)


# 删除商品
def admin_del_goods(request):
    if request.method == 'GET':
        g_id = request.GET.get('g_id')
        goods = GoodsValue.objects.filter(id=g_id).first()
        goods.isDelete = 1
        goods.save()
        data = {
            'msg': '商品删除成功'
        }
        return HttpResponseRedirect(reverse('admin_product_list'), data)


# 商品回收站
def admin_recycle_bin(request):
    if request.method == 'GET':
        num = request.GET.get('page_num', 1)
        goods = GoodsValue.objects.filter(isDelete=1)
        paginator = Paginator(goods, 2)
        pages = paginator.page(num)
        data = {
            'goods': pages
        }
        return render(request, 'admin/recycle_bin.html', data)


# 恢复商品
def admin_recover_goods(request):
    if request.method == 'GET':
        g_id = request.GET.get('g_id')
        goods = GoodsValue.objects.filter(id=g_id).first()
        goods.isDelete = 0
        goods.save()
        data = {
            'msg': '商品恢复成功'
        }
        return HttpResponseRedirect(reverse('admin_recycle_bin'), data)


# 彻底删除商品
def admin_delete_goods(request):
    if request.method == 'GET':
        g_id = request.GET.get('g_id')
        GoodsValue.objects.filter(id=g_id).delete()
        data = {
            'msg': '彻底删除成功'
        }
        return HttpResponseRedirect(reverse('admin_recycle_bin'), data)


# 查找商品
def admin_find_goods(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('admin_product_list'))


# 订单列表
def admin_order_list(request):
    if request.method == 'GET':
        return render(request, 'admin/order_list.html')


# 订单详情
def admin_order_detail(request):
    if request.method == 'GET':
        return render(request, 'admin/order_detail.html')


# 会员列表
def admin_user_list(request):
    if request.method == 'GET':
        return render(request, 'admin/user_list.html')


# 添加会员
def admin_user_detail(request):
    if request.method == 'GET':
        return render(request, 'admin/user_detail.html')


# 会员等级
def admin_user_rank(request):
    if request.method == 'GET':
        return render(request, 'admin/user_rank.html')


# 会员资金管理
def admin_adjust_funding(request):
    if request.method == 'GET':
        return render(request, 'admin/adjust_funding.html')


# 站点基础设置
def admin_setting(request):
    if request.method == 'GET':
        return render(request, 'admin/setting.html')


# 配送方式
def admin_express_list(request):
    if request.method == 'GET':
        return render(request, 'admin/express_list.html')


# 支付方式
def admin_pay_list(request):
    if request.method == 'GET':
        return render(request, 'admin/pay_list.html')


# 流量统计
def admin_discharge_statistic(request):
    if request.method == 'GET':
        return render(request, 'admin/discharge_statistic.html')


# 销售额统计
def admin_sales_volume(request):
    if request.method == 'GET':
        return render(request, 'admin/sales_volume.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        password_c = request.POST.get('cpwd')
        email = request.POST.get('email')
        # 验证参数都不能为空
        if not all([username, password, password_c, email]):
            data = {
                'msg': '请填写完整的信息'
            }
            return render(request, 'register.html', data)
        # 加密password
        password = make_password(password)
        password_c = make_password(password_c)
        # 创建用户并添加到数据库
        UserModel.objects.create(username=username,
                                 password=password,
                                 password_c=password_c,
                                 email=email)
        # 注册成功跳转到登陆页面
        return HttpResponseRedirect(reverse('login'))


# 登陆
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        data = {}
        # 验证信息是否填写完整
        if not all([username, password]):
            data['msg'] = '请填写完整的用户名或密码'
        # 验证用户是否注册
        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            # 验证密码是否正确
            if check_password(password, user.password):
                # 如果密码正确将ticket值保存在cookie中
                ticket = get_ticket()
                response = HttpResponseRedirect(reverse('admin_index'))
                out_time = datetime.now() + timedelta(days=2)
                response.set_cookie('ticket', ticket, expires=out_time)
                # 保存ticket值到数据库user_ticket表中
                UserTicketModel.objects.create(user=user,
                                               out_time=out_time,
                                               ticket=ticket)
                return response
            else:
                msg = '用户名或密码错误'
                return render(request, 'login.html', {'msg': msg})
        else:
            msg = '用户名不存在,请注册后在登陆'
            return render(request, 'login.html', {'msg': msg})


# 退出
def logout(request):
    if request.method == 'GET':
        # 退出则删除数据库中的ticket值
        ticket = request.COOKIES.get('ticket')
        user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
        UserTicketModel.objects.filter(user=user_ticket.user).delete()
        return HttpResponseRedirect(reverse('login'))

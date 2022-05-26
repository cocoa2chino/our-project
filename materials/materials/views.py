from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from django.urls import reverse
import random
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


# Create your views here.
# 登录


# 后台登录
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
        user = authenticate(username=username, password=password)
        auth.login(request, user)
        response = HttpResponseRedirect(reverse('admin_index'))
        return response


# 后台首页
def admin_index(request):
    kind = ArticleCategory.objects.create(kind="食品")
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


# 提交订单
def place_order(request):
    if request.method == 'GET':
        user = request.user
        carts = CartInfo.objects.filter(user=user)
        data = {'carts': carts}
        return render(request, 'place_order.html', data)


# 个人信息
def user_center_info(request):
    if request.method == 'GET':
        return render(request, 'user_center_info.html')


# 全部订单
def user_center_order(request):
    if request.method == 'GET':
        return render(request, 'user_center_order.html')


# 收货地址
def user_center_site(request):
    # 拿到登陆用户的id
    id = request.user.id
    user_info = UserModel.objects.filter(id=id).first()
    if request.method == 'GET':
        data = {'user_info': user_info}
        return render(request, 'user_center_site.html', data)

    if request.method == 'POST':
        recipients = request.POST.get('recipients')
        direction = request.POST.get('direction')
        addressee_p = request.POST.get('addressee_p')
        phone = request.POST.get('phone')
        # 验证信息是否填写完整
        if not all([recipients, direction, addressee_p, phone]):
            data = {'msg': '请填写完整的收货信息!',
                    'user_info': user_info}  # 避免提交表单信息为空时当前地址不显示
            return render(request, 'user_center_site.html', data)
        user_info.recipients = recipients
        user_info.direction = direction
        user_info.addressee_p = addressee_p
        user_info.phone = phone
        user_info.save()
        data = {'msg': '收货地址添加成功'}
        return HttpResponseRedirect(reverse('user_center_site'), data)


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
        User.objects.create_user(username=username,
                                password=password,
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
                response = HttpResponseRedirect(reverse('index'))
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


# 商品详情
def detail(request):
    if request.method == 'GET':
        kinds = ArticleCategory.objects.all()
        # 拿到的详情商品
        g_id = request.GET.get('g_id')
        goods = GoodsValue.objects.filter(id=g_id).first()

        # 拿到的新品推荐商品
        # pass

        data = {
            'kinds': kinds,
            'goods': goods
        }
        return render(request, 'detail.html', data)


# 增加商品数量
def add_goods(request):
    if request.method == 'POST':
        user = request.user
        data = {}
        if user.id:
            goods_id = request.POST.get('goods_id')
            # 验证当前登录用户是否对同一商品进行添加操作, 如果有则继续添加
            cart = CartInfo.objects.filter(user=user, goods_id=goods_id).first()
            if cart:
                cart.count += 1
                cart.save()
                data['count'] = cart.count
                # 计算单个商品总价
                data['goods_price'] = round(cart.goods.g_price * cart.count, 2)
            else:
                # 验证当前登陆用户有没有添加商品到购物车中，如果没有则创建
                CartInfo.objects.create(user=user, goods_id=goods_id)
                data['count'] = 1
            data['code'] = '200'
            data['msg'] = '请求成功'
            return JsonResponse(data)
        data['code'] = '1000'
        data['msg'] = '请登录后再使用'
        return JsonResponse(data)


# 减少商品数量
def sub_goods(request):
    if request.method == 'POST':
        user = request.user
        data = {}
        if user.id:
            goods_id = request.POST.get('goods_id')
            cart = CartInfo.objects.filter(user=user, goods_id=goods_id).first()
            if cart:
                if cart.count == 1:
                    # cart.delete()
                    # data['count'] = 0
                    data['msg'] = '亲! 至少买一个吧'
                else:
                    cart.count -= 1
                    cart.save()
                    data['count'] = cart.count
                    # 计算单个商品总价
                    data['goods_price'] = round(cart.goods.g_price * cart.count, 2)
                data['code'] = '200'
                data['msg'] = '请求成功'
                return JsonResponse(data)
            else:
                data['msg'] = '请添加商品'
                return JsonResponse(data)
        else:
            data['code'] = '1001'
            data['msg'] = '请登录后再使用'
            return JsonResponse(data)


# 刷新商品增添/减少数量, 单个商品总价刷新
def goods_num(request):
    if request.method == 'GET':
        user = request.user
        cart_list = []
        if user.id:
            carts = CartInfo.objects.filter(user=user)
            for cart in carts:
                data = {
                    'id': cart.id,
                    'goods_id': cart.goods.id,
                    'count': cart.count,
                    'user_id': cart.user.id,
                    # 单个商品总价
                    'goods_price': round(cart.goods.g_price * cart.count, 2)
                }
                cart_list.append(data)
            data = {
                'carts': cart_list,
                'code': '200',
                'msg': '请求成功'
            }
            return JsonResponse(data)
        else:
            data = {
                'carts': '',
                'code': '1002',
                'msg': '请登录后再使用'
            }
            return JsonResponse(data)


# 加入购物车
def add_cart(request):
    pass


# 立即购买
def buy_cart(request):
    if request.method == 'GET':
        user = request.user
        carts = CartInfo.objects.filter(user=user)
        data = {'carts': carts}
        return render(request, 'cart.html', data)


# 计算商品总价
def tatal_price(request):
    if request.method == 'GET':
        user = request.user
        # 获取购物车中的商品信息
        carts = CartInfo.objects.filter(user=user)
        tatal_price = 0
        num = 0
        for cart in carts:
            tatal_price += cart.goods.g_price * cart.count
            # 计算购物车商品件数
            num += 1
        # 总价保留2位小数
        tatal_price = round(tatal_price, 2)
        data = {
            'tatal_price': tatal_price,
            'num': num,
            'code': '200',
            'msg': '请求成功'
        }
        return JsonResponse(data)


# 删除购物车商品
def del_goods_cart(request):
    if request.method == 'GET':
        user = request.user
        cart_id = request.GET.get('cart_id')
        CartInfo.objects.filter(user=user, id=cart_id).delete()
        data = {'code': '1006',
                'msg': '删除成功'}
        return HttpResponseRedirect(reverse('buycart'), data)


def index(request):
    # 首页水果展示
    if request.method == 'GET':
        fresh_fruit = GoodsValue.objects.filter(gtype_id=1, isDelete=0)[0:4]
        seafood_aquaculture = GoodsValue.objects.filter(gtype_id=2, isDelete=0)[0:4]
        red_meat = GoodsValue.objects.filter(gtype_id=3, isDelete=0)[0:4]
        poultry_egg = GoodsValue.objects.filter(gtype_id=4, isDelete=0)[0:4]
        green_goods = GoodsValue.objects.filter(gtype_id=5, isDelete=0)[0:4]
        quick_frozen = GoodsValue.objects.filter(gtype_id=6, isDelete=0)[0:4]

        data = {
            'fresh_fruit': fresh_fruit,
            'seafood_aquaculture': seafood_aquaculture,
            'red_meat': red_meat,
            'poultry_egg': poultry_egg,
            'green_goods': green_goods,
            'quick_frozen': quick_frozen,
        }
        return render(request, 'index.html', data)


# 商品列表
def list(request):
    if request.method == 'GET':
        kinds = ArticleCategory.objects.all()
        goods = GoodsValue.objects.filter(isDelete=0)
        # 商品推荐前2名, 暂时定2个
        tj_goods = GoodsValue.objects.filter(isDelete=0)[5:8]
        data = {
            'kinds': kinds,
            'goods': goods,
            'tj_goods': tj_goods
        }
        return render(request, 'list.html', data)

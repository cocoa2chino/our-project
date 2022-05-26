"""materials URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    # 用户中心 - 用户信息页
    path('user_center_info/', views.user_center_info, name='user_center_info'),
    # 用户中心 - 用户订单页
    path('user_center_order/', views.user_center_order, name='user_center_order'),
    # 用户中心 - 用户收货地址页
    path('user_center_site/', views.user_center_site, name='user_center_site'),
    path('',views.login),
    path('admin/', admin.site.urls),
    path('admin_index/', views.admin_index, name='admin_index'),
    # 商品列表分页展示
    path('admin_product_list/', views.admin_product_list, name='admin_product_list'),
    # 添加商品
    path('admin_product_detail/', views.admin_product_detail, name='admin_product_detail'),
    # 修改商品
    path('admin_change_goods/', views.admin_change_goods, name='admin_change_goods'),
    # 删除商品
    path('admin_del_goods/', views.admin_del_goods, name='admin_del_goods'),
    # 商品回收站
    path('admin_recycle_bin/', views.admin_recycle_bin, name='admin_recycle_bin'),
    # 恢复商品
    path('admin_recover_goods/', views.admin_recover_goods, name='admin_recover_goods'),
    # 彻底删除商品
    path('admin_delete_goods/', views.admin_delete_goods, name='admin_delete_goods'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('register/', views.register, name='register'),
    # 登陆
    path('login/', views.login, name='login'),
    # 退出
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    # 商城商品列表页
    path('list/', views.list, name='list'),
    path('admin_find_goods/', views.admin_find_goods, name='admin_find_goods'),
    # 订单列表
    path('admin_order_list/', views.admin_order_list, name='admin_order_list'),
    # 订单详情
    path('admin_order_detail/', views.admin_order_detail, name='admin_order_detail'),
    path('detail/', views.detail, name='detail'),
    # 增加商品数量
    path('addgoods/', views.add_goods, name='addgoods'),
    # 减少商品数量
    path('subgoods/', views.sub_goods, name='subgoods'),
    # 刷新增添与减少商品数量
    path('goodsnum/', views.goods_num, name='goodsnum'),
    # 加入购物车
    path('addcart/', views.add_cart, name='addcart'),
    # 立即购买
    path('buycart/', views.buy_cart, name='buycart'),
    # 计算商品总价
    path('tatalprice/', views.tatal_price, name='tatalprice'),
    # 删除购物车商品
    path('delgoodscart/', views.del_goods_cart, name='delgoodscart'),
]

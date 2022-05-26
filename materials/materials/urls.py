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
    path('admin_find_goods/', views.admin_find_goods, name='admin_find_goods'),
    # 订单列表
    path('admin_order_list/', views.admin_order_list, name='admin_order_list'),
    # 订单详情
    path('admin_order_detail/', views.admin_order_detail, name='admin_order_detail'),
    # 会员列表
    path('admin_user_list/', views.admin_user_list, name='admin_user_list'),
    # 添加会员
    path('admin_user_detail/', views.admin_user_detail, name='admin_user_detail'),
    # 会员等级
    path('admin_user_rank/', views.admin_user_rank, name='admin_user_rank'),
    # 会员金管理
    path('admin_adjust_funding/', views.admin_adjust_funding, name='admin_adjust_funding'),
    # 站点基础设置
    path('admin_setting/', views.admin_setting, name='admin_setting'),
    # 配送方式
    path('admin_express_list/', views.admin_express_list, name='admin_express_list'),
    # 支付方式
    path('admin_pay_list/', views.admin_pay_list, name='admin_pay_list'),
    # 流量统计
    path('admin_discharge_statistic/', views.admin_discharge_statistic, name='admin_discharge_statistic'),
    # 销售额统计
    path('admin_sales_volume/', views.admin_sales_volume, name='admin_sales_volume'),
]

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models import CASCADE

from materials import settings


class OrderModel(models.Model):
    o_id = models.CharField(max_length=20, primary_key=True)  # 订单id
    o_user = models.ForeignKey(User, on_delete=CASCADE)  # 关联用户
    o_date = models.DateTimeField(auto_now=True)  # 订单日期
    o_address = models.CharField(max_length=150)  # 收货地址


# 创建商品属性模型
class ArticleCategory(models.Model):
    kind = models.CharField(max_length=30)  # 分类
    isDelete = models.BooleanField(default=False)  # 是否删除


class GoodsValue(models.Model):
    g_name = models.CharField(max_length=20)  # 商品名称
    g_img = models.ImageField(upload_to='shop')  # 商品图片
    g_num = models.CharField(max_length=100)  # 商品货号
    g_unit = models.CharField(max_length=20, default='500g')  # 商品单位
    g_repertory = models.IntegerField()  # 商品库存
    isDelete = models.BooleanField(default=False)  # 是否删除
    # 关联商品种类
    gtype = models.ForeignKey(ArticleCategory, on_delete=CASCADE)


# 创建订单详情表模型
class OrderDetailModel(models.Model):
    goods = models.ForeignKey(GoodsValue, on_delete=CASCADE)  # 关联商品
    order = models.ForeignKey(OrderModel, on_delete=CASCADE)  # 关联商品
    count = models.IntegerField()  # 数量
    isTrue = models.BooleanField(default=False)  # 统计销量是否统计进去


class CartInfo(models.Model):
    # 关联用户
    user = models.ForeignKey(User, on_delete=CASCADE)
    # 关联商品
    goods = models.ForeignKey(GoodsValue, on_delete=CASCADE)
    # 购买的数量
    count = models.IntegerField(default=1)

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class UserModel(models.Model):
    username = models.CharField(max_length=32, unique=True)  # 用户名
    password = models.CharField(max_length=256)  # 密码
    password_c = models.CharField(max_length=256)  # 确认密码
    email = models.CharField(max_length=64, unique=True)  # 邮箱
    recipients = models.CharField(max_length=10, default='')  # 收件人姓名
    phone = models.CharField(max_length=11, default='')  # 收件人电话
    addressee_p = models.CharField(max_length=6, default='')  # 收件人邮编
    direction = models.CharField(max_length=100, default='')  # 收件人地址


class UserTicketModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=CASCADE)  # 关联用户模型
    ticket = models.CharField(max_length=256)  # 密码
    out_time = models.DateTimeField()  # 过期时间


class AdminUserModel(models.Model):
    username = models.CharField(u'用户名', max_length=32, unique=True)  # 用户名
    password = models.CharField(u'密码', max_length=256)  # 密码


class OrderModel(models.Model):
    o_id = models.CharField(max_length=20, primary_key=True)  # 订单id
    o_user = models.ForeignKey(UserModel, on_delete=CASCADE)  # 关联用户
    o_date = models.DateTimeField(auto_now=True)  # 购买日期
    o_pay = models.BooleanField(default=False)  # 付款属性
    o_total = models.DecimalField(max_digits=6, decimal_places=2)  # 总价
    o_address = models.CharField(max_length=150)  # 收货地址


# 创建订单表模型
class OrderModel(models.Model):
    o_id = models.CharField(max_length=20, primary_key=True)  # 订单id
    o_user = models.ForeignKey(UserModel, on_delete=CASCADE)  # 关联用户
    o_date = models.DateTimeField(auto_now=True)  # 购买日期
    o_pay = models.BooleanField(default=False)  # 付款属性
    o_total = models.DecimalField(max_digits=6, decimal_places=2)  # 总价
    o_address = models.CharField(max_length=150)  # 收货地址

    class Meta:
        db_table = "sx_order"


# 创建商品属性模型
class ArticleCategory(models.Model):
    kind = models.CharField(max_length=30)  # 分类
    isDelete = models.BooleanField(default=False)  # 是否删除


class GoodsValue(models.Model):
    g_name = models.CharField(max_length=20)  # 商品名称
    g_img = models.ImageField(upload_to='shop')  # 商品图片
    g_num = models.CharField(max_length=100)  # 商品货号
    g_price = models.FloatField(default=0)  # 商品价格
    g_unit = models.CharField(max_length=20, default='500g')  # 商品单位
    g_repertory = models.IntegerField()  # 商品库存
    isDelete = models.BooleanField(default=False)  # 是否删除
    # 关联商品种类
    gtype = models.ForeignKey(ArticleCategory, on_delete=CASCADE)


# 创建订单详情表模型
class OrderDetailModel(models.Model):
    goods = models.ForeignKey(GoodsValue, on_delete=CASCADE)  # 关联商品
    order = models.ForeignKey(OrderModel, on_delete=CASCADE)  # 关联商品
    price = models.DecimalField(max_digits=5, decimal_places=2)  # 总价
    count = models.IntegerField()  # 数量
    isTrue = models.BooleanField(default=False)  # 统计销量是否统计进去

    class Meta:
        db_table = "sx_order_detail"


class CartInfo(models.Model):
    # 关联用户
    user = models.ForeignKey(UserModel, on_delete=CASCADE)
    # 关联商品
    goods = models.ForeignKey(GoodsValue, on_delete=CASCADE)
    # 购买的数量
    count = models.IntegerField(default=1)

    class Meta:
        db_table = "sx_cart"

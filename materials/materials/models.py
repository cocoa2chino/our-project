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


class Materials(models.Model):
    # 物资信息储存
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    materials_name = models.CharField(max_length=20, primary_key=True)  # 物资名称
    materials_int = models.IntegerField()  # 物资数量
    materials_type = models.CharField(max_length=20)  # 物资类型

    def __str__(self):
        return self.materials_name


class Requests(models.Model):
    # 存储请求信息
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 发出请求的用户对象
    materials = models.ForeignKey(Materials, on_delete=models.CASCADE)  # 请求的物资对象
    materials_req_time = models.DateTimeField()  # 请求分发时间
    materials_req_int = models.IntegerField()  # 请求物资数量
    materials_text = models.TextField()  # 对物资的文字备注
    materials_time = models.DateTimeField(auto_now_add=True)  # 请求时间，已设置自动添加

    def __str__(self):
        return str(self.materials_text)


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

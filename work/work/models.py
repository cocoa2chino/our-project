import datetime

from django.db import models




class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    repassword = models.CharField(max_length=256)
    email = models.EmailField(max_length=30, unique=True)
    icon = models.ImageField(upload_to='icons/%Y/%m/%d/', null=True,default='icons/haha.jpg')
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    rank = models.IntegerField(default=0)

    tel = models.PositiveIntegerField(blank=True, null=True)
    qq = models.CharField(max_length=20, blank=True, null=True)
    wechat = models.CharField(max_length=20, blank=True, null=True)
    other = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'smh_user'

# Create your models here.
class entry_bill(models.Model):
    entry_id = models.AutoField(primary_key=True)
    goods_id = models.CharField(max_length=10)
    storage_id = models.CharField(max_length=10)
    supplier_id = models.CharField(max_length=10)
    goods_price = models.CharField(max_length=12)
    goods_num = models.CharField(max_length=10)
    entry_data = models.DateField(max_length=10)


class goods(models.Model):
    goods_id = models.AutoField(primary_key=True)
    goods_name = models.CharField(max_length=10)
    goods_sort = models.CharField(max_length=10)
    goods_num = models.CharField(max_length=10)
    goods_remark = models.CharField(max_length=10)


# Create your models here.
class out_bill(models.Model):
    out_id = models.AutoField(primary_key=True)
    goods_id = models.CharField(max_length=10)
    storage_id = models.CharField(max_length=10)
    subscriber_id = models.CharField(max_length=10)
    goods_price = models.CharField(max_length=10)
    goods_num = models.CharField(max_length=10)
    out_data = models.DateField(max_length=10)


class subscriber(models.Model):
    subscriber_id = models.AutoField(primary_key=True)
    subscriber_name = models.CharField(max_length=10)


class storage(models.Model):
    storage_id = models.AutoField(primary_key=True)
    storage_name = models.CharField(max_length=10)


class supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=10)

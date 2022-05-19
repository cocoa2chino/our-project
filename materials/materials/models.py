from django.contrib.auth.models import User
from django.db import models


class Materials(models.Model):
    # 物资信息储存
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

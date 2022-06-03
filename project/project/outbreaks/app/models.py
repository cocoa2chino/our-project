from django.db import models

class Notices(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    title = models.CharField('通知标题',  max_length=32, null=False)
    detail = models.CharField('通知详情', max_length=125, null=False)
    createTime = models.CharField('通知时间', db_column='create_time', max_length=19)
    class Meta:
        db_table = 'notices'

class Statistics(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    createTime = models.CharField('统计时间', db_column='create_time', max_length=10)
    confirm = models.IntegerField('累计确诊',  null=False)
    heal = models.IntegerField('累计治愈', null=False)
    dead = models.IntegerField('累计死亡', null=False)
    nowConfirm = models.IntegerField('当前确诊', db_column='now_confirm', null=False)
    class Meta:
        db_table = 'statistics'

class Users(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    userName = models.CharField('用户账号', db_column='user_name', max_length=32, null=False)
    passWord = models.CharField('用户密码', db_column='pass_word', max_length=32, null=False)
    name = models.CharField('用户姓名', max_length=20, null=False)
    gender = models.CharField('用户性别', max_length=4, null=False)
    age = models.IntegerField('用户年龄', null=False)
    phone = models.CharField('联系电话', max_length=11, null=False)
    address = models.CharField('联系地址', max_length=64, null=False)
    type = models.IntegerField('用户身份', null=False)
    class Meta:
        db_table = 'users'

class CheckLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    createTime = models.CharField('检查时间', db_column='create_time', max_length=19)
    loc = models.CharField('检查地点',  max_length=64, null=False)
    resl = models.CharField('检查结果',  max_length=2, null=False)
    detail = models.CharField('检查详情', max_length=125, null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column="user_id")
    class Meta:
        db_table = 'check_logs'

class AbnormityLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    createTime = models.CharField('登记时间', db_column='create_time', max_length=19)
    detail = models.CharField('检查详情', max_length=125, null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column="user_id")
    class Meta:
        db_table = 'abnormity_logs'

class VaccinateLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('接种人姓名', max_length=20, null=False)
    card = models.CharField('身份证号', max_length=18, null=False)
    phone = models.CharField('联系电话', max_length=11, null=False)
    address = models.CharField('联系地址', max_length=64, null=False)
    vaccinateNo = models.CharField('接种次数', db_column='vaccinate_no', max_length=4, null=False)
    vaccinateTime = models.CharField('接种时间', db_column='vaccinate_time', max_length=10, null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column="user_id")
    class Meta:
        db_table = 'vaccinate_logs'
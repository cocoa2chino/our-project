# Generated by Django 4.0.4 on 2022-05-29 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notices',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录编号')),
                ('title', models.CharField(max_length=32, verbose_name='通知标题')),
                ('detail', models.CharField(max_length=125, verbose_name='通知详情')),
                ('createTime', models.CharField(db_column='create_time', max_length=19, verbose_name='通知时间')),
            ],
            options={
                'db_table': 'notices',
            },
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录编号')),
                ('createTime', models.CharField(db_column='create_time', max_length=10, verbose_name='统计时间')),
                ('confirm', models.IntegerField(verbose_name='累计确诊')),
                ('heal', models.IntegerField(verbose_name='累计治愈')),
                ('dead', models.IntegerField(verbose_name='累计死亡')),
                ('nowConfirm', models.IntegerField(db_column='now_confirm', verbose_name='当前确诊')),
            ],
            options={
                'db_table': 'statistics',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录编号')),
                ('userName', models.CharField(db_column='user_name', max_length=32, verbose_name='用户账号')),
                ('passWord', models.CharField(db_column='pass_word', max_length=32, verbose_name='用户密码')),
                ('name', models.CharField(max_length=20, verbose_name='用户姓名')),
                ('gender', models.CharField(max_length=4, verbose_name='用户性别')),
                ('age', models.IntegerField(verbose_name='用户年龄')),
                ('phone', models.CharField(max_length=11, verbose_name='联系电话')),
                ('address', models.CharField(max_length=64, verbose_name='联系地址')),
                ('type', models.IntegerField(verbose_name='用户身份')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='VaccinateLogs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录编号')),
                ('name', models.CharField(max_length=20, verbose_name='接种人姓名')),
                ('card', models.CharField(max_length=18, verbose_name='身份证号')),
                ('phone', models.CharField(max_length=11, verbose_name='联系电话')),
                ('address', models.CharField(max_length=64, verbose_name='联系地址')),
                ('vaccinateNo', models.CharField(db_column='vaccinate_no', max_length=4, verbose_name='接种次数')),
                ('vaccinateTime', models.CharField(db_column='vaccinate_time', max_length=10, verbose_name='接种时间')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='app.users')),
            ],
            options={
                'db_table': 'vaccinate_logs',
            },
        ),
        migrations.CreateModel(
            name='CheckLogs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录编号')),
                ('createTime', models.CharField(db_column='create_time', max_length=19, verbose_name='检查时间')),
                ('loc', models.CharField(max_length=64, verbose_name='检查地点')),
                ('resl', models.CharField(max_length=2, verbose_name='检查结果')),
                ('detail', models.CharField(max_length=125, verbose_name='检查详情')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='app.users')),
            ],
            options={
                'db_table': 'check_logs',
            },
        ),
        migrations.CreateModel(
            name='AbnormityLogs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录编号')),
                ('createTime', models.CharField(db_column='create_time', max_length=19, verbose_name='登记时间')),
                ('detail', models.CharField(max_length=125, verbose_name='检查详情')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='app.users')),
            ],
            options={
                'db_table': 'abnormity_logs',
            },
        ),
    ]
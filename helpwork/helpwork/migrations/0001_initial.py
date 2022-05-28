# Generated by Django 3.1.7 on 2022-05-28 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.IntegerField(default=0)),
                ('typename', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'smh_contact_type',
            },
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.IntegerField(default=1)),
                ('typename', models.CharField(max_length=32)),
                ('typesort', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'smh_tasktype',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('repassword', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('icon', models.ImageField(default='icons/haha.jpg', null=True, upload_to='icons/%Y/%m/%d/')),
                ('is_active', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('rank', models.IntegerField(default=0)),
                ('tel', models.PositiveIntegerField(blank=True, null=True)),
                ('qq', models.CharField(blank=True, max_length=20, null=True)),
                ('wechat', models.CharField(blank=True, max_length=20, null=True)),
                ('other', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'smh_user',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=32)),
                ('task_sketch', models.CharField(blank=True, max_length=512, null=True)),
                ('task_file', models.FileField(blank=True, null=True, upload_to='task_file/%Y/%m/%d/')),
                ('task_time', models.DateField(blank=True, null=True)),
                ('task_reward', models.FloatField(blank=True, default=0, null=True)),
                ('is_pickedup', models.BooleanField(default=False)),
                ('is_finished', models.BooleanField(default=False)),
                ('is_overtime', models.BooleanField(default=False)),
                ('comment_publisher', models.CharField(blank=True, max_length=1000, null=True)),
                ('comment_hunter', models.CharField(blank=True, max_length=1000, null=True)),
                ('contact_type_hunter', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_hunter', to='helpwork.contact', verbose_name='委托人联系方式')),
                ('contact_type_publisher', models.ForeignKey(blank=True, db_constraint=False, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_publisher', to='helpwork.contact', verbose_name='发布人联系方式')),
                ('hunter', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='hunter', to='helpwork.user', verbose_name='委托人')),
                ('publisher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publisher', to='helpwork.user', verbose_name='发布人')),
                ('task_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='helpwork.tasktype')),
            ],
            options={
                'db_table': 'smh_task',
            },
        ),
        migrations.CreateModel(
            name='Revoke_reason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revoke_reason', models.CharField(max_length=512, null=True)),
                ('task', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='revoked_tasks', to='helpwork.task')),
            ],
            options={
                'db_table': 'smh_reason',
            },
        ),
        migrations.CreateModel(
            name='Cancel_reason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancel_reason', models.CharField(max_length=512, null=True)),
                ('task', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='canceled_tasks', to='helpwork.task')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='user_canceled', to='helpwork.user')),
            ],
        ),
    ]

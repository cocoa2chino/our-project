"""helpwork URL Configuration

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
    path('', views.task_square),
    path('admin/', admin.site.urls),  # 后台界面
    path('logon/', views.index, name='index'),  # 注册
    path('login/', views.login, name='login'),  # 登录
    path('edit', views.edit0, name='edit'),  # 个人信息修改
    path('up0/', views.task_up, name='up0'),  # 提交求助

    path('task_received/', views.all_task_received),
    path('all_task_received/', views.all_task_received, name='all_task_received'),  # 全部已接受的求助
    path('<int:task_id>/task_revoke/', views.task_revoke, name='task_revoke'),  # 撤销求助
    path('<int:task_id>/task_revoke/reasons/', views.reasons_revoke, name='reasons_revoke'),  # 填写撤销原因
    path('<int:task_id>/task_detail', views.task_detail, name='task_detail'),  # 任务详情
    path('<int:task_id>/task_finished', views.task_finished, name='task_finished'),  # 完成求助任务
    path('all_task_received/<int:tasktype_id>/', views.task_sometype, name='task_sometype'),  # 分类展示已接受的求助
    path('received_tasks_finished/', views.received_tasks_finished, name='received_tasks_finished'),  # 求助已完成
    path('received_tasks_finished/<int:tasktype_id>/', views.task_sometype_finished, name='task_sometype_finished'),
    # 分类展示已完成的求助
    path('received_tasks_not_finished/', views.received_tasks_not_finished, name='received_tasks_not_finished'),
    path('received_tasks_not_finished/<int:tasktype_id>', views.task_sometype_not_finished,
         name='task_sometype_not_finished'),
    path('comment/', views.comment, name='comment'),
    path('revoke/', views.revoke, name='revoke'),
    path('logout/', views.logout, name='logout'),
    path('admin/', admin.site.urls),
    path('acp', views.acp),
    path('finish', views.finish),
    path('un_acp', views.un_acp),
    path('f_mission/', views.f_mission),
    path('d_mission/', views.d_mission),
    path('comment', views.comment),
    path('reason', views.reason),
    path('d_unacpm/', views.d_unacpm),
    path('m_detail/', views.m_detail),
    path('m_change', views.m_change),
    path('download/', views.download),
    path('change_one', views.change_one),
    path('task_square/', views.task_square, name='task_square'),
    path('sort/<int:type_id>/<slug:order>', views.task_square_sort, name='task_square_sort'),
    path('check_hunt/<int:task_id>/', views.check_hunt, name='check_hunt'),
    path('hunt_task/<int:task_id>/', views.hunt_task, name='hunt_task'),
    path('<int:task_id>/task_details/', views.task_details, name='task_details'),
    path('<int:publisher_id>/publisher_detail/', views.publisher_detail, name='publisher_detail'),
    path('findtasks/', views.findtasks, name='findtasks'),
    path('downloadnew/<int:task_id>/', views.downloadnew, name="downloadnew"),

]

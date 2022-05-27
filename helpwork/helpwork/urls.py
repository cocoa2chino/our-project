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
    path('admin/', admin.site.urls),
    path('logon/', views.index, name='index'),
    # 注册,
    path('login/', views.login, name='login'),
    # 登录
    path('edit', views.edit0, name='edit'),
    # 个人信息修改
    path('up0/', views.task_up, name='up0'),
    path('', views.login),
    path('task_square/', views.task_square, name='task_square'),
    path('task_square/sort/<int:type_id>/<slug:order>', views.task_square_sort, name='task_square_sort'),
    path('task_square/findtasks/', views.findtasks, name='findtasks'),
    path('all_task_received/', views.all_task_received, name='all_task_received'),
    path('logout/',views.logout,name='logout'),
]

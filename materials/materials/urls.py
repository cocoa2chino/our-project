"""materials URL Configuration

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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from .views import loginView, regView, indexPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', loginView),
    path('', indexPage, name='home'),  # 登录，默认访问 127.0.0.1:8000 时展示登录界面
=======
=======
>>>>>>> parent of 1f3e252 (登录注册完成)
=======
>>>>>>> parent of 1f3e252 (登录注册完成)
from views import loginView, regView, index
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.loginView),
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> parent of 1f3e252 (登录注册完成)
=======
>>>>>>> parent of 1f3e252 (登录注册完成)
=======
>>>>>>> parent of 1f3e252 (登录注册完成)
    path('reg/', regView),
    path('index/', indexPage),
]

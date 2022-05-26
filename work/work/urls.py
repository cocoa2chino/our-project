"""work URL Configuration

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
    path('entry_storage/', views.entry_storage),
    path('entry_storage_delete/', views.entry_storage_delete),
    path('goods/', views.goods),
    path('goods_delete/', views.goods_delete),
    path('out_storage/', views.out_storage),
    path('out_storage_delete/', views.out_storage_delete),
    path('storage/', views.subscriber),
    path('storage_delete/', views.subscriber_delete),
    path('subscriber/', views.subscriber),
    path('subscriber_delete/', views.subscriber_delete),
    path('supplier/', views.supplier),
    path('supplier_delete/', views.supplier_delete),
]

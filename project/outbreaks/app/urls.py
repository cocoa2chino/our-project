import app.views

from django.urls import path

urlpatterns = [
    path('<str:module>/', app.views.SysView.as_view()),  # 系统处理路由
    path('notices/<str:module>/', app.views.NoticesView.as_view()),  # 求助信息路由
    path('check/<str:module>/', app.views.CheckLogsView.as_view()),  # 出入库路由
    path('vaccinate/<str:module>/', app.views.VaccinateLogsView.as_view()),  # 物资管理路由
    path('abnormity/<str:module>/', app.views.AbnormityLogsView.as_view()),  # 异常处理路由
    path('statistics/<str:module>/', app.views.StatisticsView.as_view()),  # 统计数据路由
    path('users/<str:module>/', app.views.UsersView.as_view())  # 用户路由
]

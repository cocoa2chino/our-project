import app.views

from django.urls import path

urlpatterns = [
    path('<str:module>/', app.views.SysView.as_view()),
    path('notices/<str:module>/', app.views.NoticesView.as_view()),
    path('check/<str:module>/', app.views.CheckLogsView.as_view()),
    path('vaccinate/<str:module>/', app.views.VaccinateLogsView.as_view()),
    path('abnormity/<str:module>/', app.views.AbnormityLogsView.as_view()),
    path('statistics/<str:module>/', app.views.StatisticsView.as_view()),
    path('users/<str:module>/', app.views.UsersView.as_view())
]

""" Adel Liu 180111

用户APi子路由
"""
from django.urls import path

from User import views

urlpatterns = [
    path('', views.UserV.as_view()),
    path('ss', views.SSV.as_view()),
]

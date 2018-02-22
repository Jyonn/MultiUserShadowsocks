""" Adel Liu 180222

用户API子路由
"""
from django.urls import path

from User.router import rt_user, rt_user_token

urlpatterns = [
    path('', rt_user),
    path('token', rt_user_token),
]

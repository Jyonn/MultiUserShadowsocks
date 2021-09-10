""" Adel Liu 180222

api子路由
"""
from django.urls import path, include

urlpatterns = [
    path('user/', include('User.urls')),
    path('oauth/', include('OAuth.urls')),
]

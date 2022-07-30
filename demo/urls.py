"""
@author: haiwen
@date: 2021/10/9
@file: urls.py
"""
from django.urls import path
from demo import views
#子路由列表
urlpatterns=[
    path('index/',views.index),
    path('home/',views.home),
]
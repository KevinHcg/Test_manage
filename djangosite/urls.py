"""djangosite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from demo import urls as demo_urls  #导入子路由模块
from sgin import urls as sgin_urls
from sgin import views
urlpatterns = [
    path('',views.login),# 进入登录页面
    path('login_action/',views.login_action),# 登录
    path('register_action/',views.register_action),# 注册
    path('logout/',views.logout),
    path('admin/', admin.site.urls),
    #参数1：访问的路径, 参数2：对应的视图函数(不要加括号)
    # path('index/',views.index),
    # path('home/',views.home),
    path('demo/',include(demo_urls)),

    # path('events/',sgin_view.events),  #发布会管理页面
    # path('events/detail',sgin_view.event_detail),
    path('sgin/',include(sgin_urls)),
]

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# 视图函数--处理用户的请求
# 必须接收的参数是request,代表用户的请求
# 返回httprespones

def index(request):

    return HttpResponse('hello django')


def home(request):
    return HttpResponse('<h1>这里是主页</h1>')
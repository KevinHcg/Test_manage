"""
@author: haiwen
@date: 2021/10/9
@file: urls.py
"""
from django.urls import path
from sgin import views

app_name = 'sgin'
#子路由列表
urlpatterns=[
    path('/',views.login),
    path('home/',views.home),
    path('events/',views.events),  #发布会管理页面
    path('events/<int:event_id>',views.event_detail), #events/8

    path('guests/',views.guests), #嘉宾管理页面
    path('guests/<int:guest_id>',views.guest_detail),

    #签到路由
    path('do_sgin/<int:event_id>',views.do_sgin),
    # 签到成功页
    path('sgin_success/<int:phone>',views.sgin_success_page),

    # 添加发布会表单页面
    path('add_event_page/',views.add_event_page),
    path('add_event/',views.add_event),

    path('add_guest/',views.add_guest),
    path('add_guest_page/',views.add_guest),

    # 需求管理页面
    path('demand/',views.demand),
    # 需求详情
    path('demand/<int:demand_id>',views.demand_detail),

    # 添加需求
    path('add_demand/',views.add_demand),
    path('add_demand_page/', views.add_demand),

    # 提测
    path('measure/<int:demand_id>',views.measure),
    path('measure/',views.measure),

    # 单需求报告
    path('single_demand_report/<int:demand_id>', views.single_demand_report),
    path('single_demand_report/', views.single_demand_report),
    path('search_demand/',views.search_demand),
    # 单报告详情
    path('single_report_detail/<int:demand_id>', views.single_report_detail),

    # 产品编辑修改
    path('product_revise/',views.product_revise),
    path('product_revise/<int:demand_id>', views.product_revise),
    # 前端完成信息
    path('front_end_completion/',views.front_end_completion),
    path('front_end_completion/<int:demand_id>', views.front_end_completion),
    # 后端完成信息
    path('backend_completion/', views.backend_completion),
    path('backend_completion/<int:demand_id>', views.backend_completion),
    # 联调完成信息
    path('combined_commissioning_completion/', views.combined_commissioning_completion),
    path('combined_commissioning_completion/<int:demand_id>', views.combined_commissioning_completion),
    # 测试完成信息
    path('test_completion/', views.test_completion),
    path('test_completion/<int:demand_id>', views.test_completion),

    # 上传用例文件
    path('upload/',views.index_view),
    path('upload/<int:demand_id>',views.index_view),
    path('demand/download/<int:file_id>', views.download_view,name="download"),

    # 获取市级信息
    # path(r'city/(\d+)',views.city,name='city'),
    # 三级联动
    path('test_multi_select',views.test_multi_select,name='test_multi_select'),

    path('get_pro/',views.get_pro),
    # path('get_city/(\d+)',views.get_city,name='get_city'),
    path('get_city/<int:pro_id>',views.get_city,name='get_city'),

    path('version/',views.version), #版本管理页面
    path('add_version/', views.add_version),
    path('add_version_page/', views.add_version),
    path('version/<int:version_id>',views.version_detail),

    # 报告
    path('report/', views.report),
    path('add_report/',views.add_report),
    path('add_report_page/',views.add_report),
    path('report/<int:report_id>', views.report_detail),

]
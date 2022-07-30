from django.db import transaction
from django.http import HttpResponse, FileResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
# 分页
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage

from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from sgin.forms import *
from sgin.models import *
import os
from sgin.config_weixin_wenzi import *


# 进入登陆页面
def login(request):
    return render(request, 'login.html')

# 开始登陆
def login_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']
    # 开始 联通 django 用户库，查看用户名密码是否正确
    from django.contrib import auth
    user = auth.authenticate(username=u_name,password=p_word)
    if user is not  None:
        # 进行正确的动作
        auth.login(request, user)
        request.session['user'] = u_name
        return HttpResponse('成功')
    else:
        # 返回前端告诉前端用户名/密码不对
        return HttpResponse('失败')

# 注册
def register_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']
    # 开始 联通django用户表
    from django.contrib.auth.models import User
    try:
        user = User.objects.create_user(username=u_name,password=p_word)
        user.save()
        return HttpResponse('注册成功!')
    except:
        return HttpResponse('注册失败～用户名好像已经存在了～')

# 退出登陆
def logout(request):
    from django.contrib import auth
    auth.logout(request)
    return HttpResponseRedirect('/')


def events(request):
    # 从数据库获取实时的数据
    event_l = Event.objects.all()
    paginator = Paginator(event_l, 10)
    # 简单的返回字符串
    # return HttpResponse([f'<li>{event}</li>' for event in event_list])
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            event_list = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            event_list = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            event_list = paginator.page(paginator.num_pages)
        # 返回一个模板内容
        return render(request,'events.html',{'event_list':event_list})

def version(request):
    # 从数据库获取实时的数据
    version_l = Version.objects.all()
    paginator = Paginator(version_l, 10)
    # 简单的返回字符串
    # return HttpResponse([f'<li>{event}</li>' for event in event_list])
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            version_list = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            version_list = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            version_list = paginator.page(paginator.num_pages)

        # 返回一个模板内容
        return render(request,'version.html',{'version_list':version_list})


#发布会详情页
def event_detail(request,event_id):
    # 从某处获取到当前页面的发布会数据对象
    try:
        event = Event.objects.get(id=event_id)
    except:
        return render(request,'404.html')

    return render(request,'event_detail.html',{'event':event})


#嘉宾
def guests(request):
    # 从数据库获取嘉宾数据
    guest_list = Guest.objects.all()
    # 返回模板页面展示嘉宾数据
    return render(request,'guests.html',{'guest_list':guest_list})


#嘉宾详情
def guest_detail(request,guest_id):
    # 获取单个嘉宾数据
    try:
        guest = Guest.objects.get(id=guest_id)
    except:
        return render(request,'404.html')

    return render(request,'guest_detail.html',{'guest':guest})

# 处理签到
@csrf_exempt
def do_sgin(request,event_id):
    # 拿到待签到的发布会
    event =Event.objects.get(pk=event_id)
    # 拿到手机号，获取签到的嘉宾
    if request.method =='POST': # 请求方法是POST并且是表单格式的数据
        phone = request.POST['phone']
        # 判断手机号是否正确
        res=Guest.objects.filter(phone=phone)
        if not res:
            #手机号错误
            return render(request,'event_detail.html',{'error':'手机号错误','event':event})
        guest = res[0]
        # 是否是当前发布会的嘉宾
        event_list = guest.events.all()
        if event not in event_list: #判断关联的发布会列表中是否存在当前签到的发布会
            return render(request,'event_detail.html',{'error':'非当前发布会嘉宾','event':event})

        # 是否已经签到
        # 取出对应的中间模型--由操作嘉宾变为操作中间模型
        ge = GuestEvent.objects.get(guest=guest,event=event)
        if ge.is_sgin:
            return render(request,'event_detail.html',{'error':'已签到，不要重复提交','event':event})
        # 执行签到
        try:
            ge.is_sgin=True
            ge.save()
        except:
            return render(request,'event_detail.html',{'error':'签到失败，服务器异常','event':event})

        # 重定向到另一个路由
        return redirect(f'/sgin/sgin_success/{phone}')


def sgin_success_page(request,phone):
    return render(request,'sgin_success.html',{'phone':phone})


def add_event_page(request):
    return render(request,'event_add.html')


def add_event(request):
    #获取发布会数据
    if request.method == 'POST':
        name = request.POST['name']
        summary = request.POST['summary']
        environment = request.POST['environment']
        # limits = request.POST['limits']
        if request.POST.get('status',False):
            status=True
        else:
            status=False


        #创建发布会
        try:
            event = Event.objects.create(name=name,summary=summary,environment=environment,status=status)
        except Exception as e:
            return render(request,'event_add.html',{'error':repr(e)}) # repr获取异常的精简信息

        #保存成功
        return redirect('/sgin/events/')

#新增嘉宾
def add_guest(request):
    # 返回新增表单页面
    if request.method == 'GET':
        event_list = Event.objects.all()
        return render(request,'guest_add.html',{'events':event_list})
    # 处理新增请求表单
    if request.method =='POST':
        #姓名
        name = request.POST['name']
        #手机号
        phone = request.POST['phone']
        #邮箱
        email = request.POST['email']
        #关联发布会
        # event_id = request.POST['event_id']
        # event_ids = request.POST['event_ids']  #这种方式只能获取到最后一个参数名为event_ids的值--错误的方式
        event_ids = request.POST.getlist('event_ids') # 获取值的列表
    #创建嘉宾
        try:
            #事务：创建嘉宾+关联发布会
            with transaction.atomic():
                guest = Guest.objects.create(name=name,phone=phone,email=email)
                #在中间表增加关联关系
                event_list = [Event.objects.get(pk=event_id) for event_id in event_ids] # 发布会数据对象列表
                # 方式1
                guest.events.add(*event_list) #单纯的添加
                # 方式2
                #guest.events.set(event_list)  # 有覆盖的作用

        except Exception as e:
            return render(request,'guest_add.html',{'error': repr(e)}) #返回精简错误信息
        #保存成功-跳转到嘉宾列表页
        return redirect('/sgin/guests/')

#新增嘉宾
def add_version(request):
    # 返回新增表单页面
    if request.method == 'GET':
        event_list = Event.objects.all()
        return render(request,'version_add.html',{'events':event_list})
    # 处理新增请求表单
    if request.method =='POST':
        #版本好
        version_name = request.POST['version_name']
        event_ids = request.POST.getlist('event_ids') # 获取值的列表
    #创建嘉宾
        try:
            #事务：创建嘉宾+关联发布会
            with transaction.atomic():
                version = Version.objects.create(version_name=version_name)
                #在中间表增加关联关系
                event_list = [Event.objects.get(pk=event_id) for event_id in event_ids] # 发布会数据对象列表
                # 方式1
                version.events.add(*event_list) #单纯的添加
                # 方式2
                #guest.events.set(event_list)  # 有覆盖的作用

        except Exception as e:
            return render(request,'version_add.html',{'error': repr(e)}) #返回精简错误信息
        #保存成功-跳转到嘉宾列表页
        return redirect('/sgin/version/')

#发布会详情页
def version_detail(request,version_id):
    # 从某处获取到当前页面的发布会数据对象
    try:
        version = Version.objects.get(id=version_id)
    except:
        return render(request,'404.html')

    return render(request,'version_detail.html',{'version':version})



# def add_demand_page(request):
#     return render(request,'demand_add.html')

#需求管理页面
def demand(request):

    # 从数据库获取需求数据
    demand_l = Demand.objects.all()
    event_list = Event.objects.all()
    paginator = Paginator(demand_l, 10)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            demand_list = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            demand_list = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            demand_list = paginator.page(paginator.num_pages)
    # 返回模板页面展示需求数据
        return render(request,'demand.html',{'demand_list':demand_list,'events':event_list})

# 需求详情页面
def demand_detail(request,demand_id):
    # 获取单个嘉宾数据
    try:
        demand = Demand.objects.get(id=demand_id)
    except:
        return render(request,'404.html')

    return render(request,'demand_detail.html',{'demand':demand})

# 添加需求
def add_demand(request):
    # 返回新增表单页面
    if request.method == 'GET':
        event_list = Event.objects.all()
        return render(request, 'demand_add.html', {'events': event_list})
    # 处理新增请求表单
    if request.method == 'POST':
        # 姓名
        name = request.POST['name']
        # 手机号
        version = request.POST['version']
        # 邮箱
        state = 0
        priority = request.POST['priority']
        describe = request.POST['describe']
        product_manager=request.POST['product_manager']
        prd_expected_start_time=request.POST['prd_expected_start_time']
        prd_expected_completion_time=request.POST['prd_expected_completion_time']
        backend_developers=request.POST['backend_developers']
        backend_expected_start_time=request.POST['backend_expected_start_time']
        backend_expected_completion_time=request.POST['backend_expected_completion_time']
        front_end_developer=request.POST['front_end_developer']
        front_end_expected_start_time=request.POST['front_end_expected_start_time']
        front_end_expected_completion_time=request.POST['front_end_expected_completion_time']
        combined_commissioning_expected_start_time=request.POST['combined_commissioning_expected_start_time']
        combined_commissioning_expected_completion_time=request.POST['combined_commissioning_expected_completion_time']
        expected_measure_time=request.POST['expected_measure_time']
        tester=request.POST['tester']
        test_expected_start_time=request.POST['test_expected_start_time']
        test_expected_completion_time=request.POST['test_expected_completion_time']

        write_cases=request.POST['write_cases']
        cases_expected_start_time=request.POST['cases_expected_start_time']
        cases_expected_completion_time=request.POST['cases_expected_completion_time']

        # 关联发布会
        event_id = request.POST['event_ids']
        # event_ids = request.POST['event_ids']  #这种方式只能获取到最后一个参数名为event_ids的值--错误的方式
        event_ids = request.POST.getlist('event_ids')  # 获取值的列表
        # if prd_expected_start_time =='' or prd_expected_completion_time =='' or backend_expected_start_time =='' or backend_expected_completion_time=='' or front_end_expected_start_time=='' or front_end_expected_completion_time=='' or combined_commissioning_expected_start_time=='' or combined_commissioning_expected_completion_time=='' or expected_measure_time=='' or test_expected_start_time=='' or test_expected_completion_time=='':
        #     test_expected_completion_time = '2002-01-01T01:01'
        #     test_expected_start_time = '2002-01-01T01:01'
        #     expected_measure_time = '2002-01-01T01:01'
        #     combined_commissioning_expected_completion_time = '2002-01-01T01:01'
        #     combined_commissioning_expected_start_time = '2002-01-01T01:01'
        #     front_end_expected_completion_time = '2002-01-01T01:01'
        #     front_end_expected_start_time = '2002-01-01T01:01'
        #     backend_expected_completion_time='2002-01-01T01:01'
        #     backend_expected_start_time='2002-01-01T01:01'
        #     prd_expected_completion_time='2002-01-01T01:01'
        #     prd_expected_start_time='2002-01-01T01:01'

        #     try:
        #         # 事务：创建嘉宾+关联发布会
        #         with transaction.atomic():
        #             demand = Demand.objects.create(name=name,version=version,state=state,priority=priority,describe=describe,product_manager=product_manager,
        #                                        prd_expected_start_time=prd_expected_start_time,prd_expected_completion_time=prd_expected_completion_time,
        #                                        backend_developers=backend_developers,backend_expected_start_time=backend_expected_start_time,
        #                                        backend_expected_completion_time=backend_expected_completion_time,front_end_developer=front_end_developer,
        #                                        front_end_expected_start_time=front_end_expected_start_time,front_end_expected_completion_time=front_end_expected_completion_time,
        #                                        combined_commissioning_expected_start_time=combined_commissioning_expected_start_time,
        #                                        combined_commissioning_expected_completion_time=combined_commissioning_expected_completion_time,
        #                                        expected_measure_time=expected_measure_time,tester=tester,test_expected_start_time=test_expected_start_time,
        #                                        test_expected_completion_time=test_expected_completion_time,event_id=event_id)
        #             # 在中间表增加关联关系
        #             event_list = [Event.objects.get(pk=event_id) for event_id in event_ids]  # 发布会数据对象列表
        #             # 方式1
        #             demand.events.add(*event_list)  # 单纯的添加
        #             # 方式2
        #             # guest.events.set(event_list)  # 有覆盖的作用
        #
        #     except Exception as e:
        #         return render(request, 'demand_add.html', {'error': repr(e)})  # 返回精简错误信息
        # else:

        try:
            # 事务：创建嘉宾+关联发布会
            with transaction.atomic():
                demand = Demand.objects.create(name=name,version=version,state=state,priority=priority,describe=describe,product_manager=product_manager,
                                               prd_expected_start_time=prd_expected_start_time,prd_expected_completion_time=prd_expected_completion_time,
                                               backend_developers=backend_developers,backend_expected_start_time=backend_expected_start_time,
                                               backend_expected_completion_time=backend_expected_completion_time,front_end_developer=front_end_developer,
                                               front_end_expected_start_time=front_end_expected_start_time,front_end_expected_completion_time=front_end_expected_completion_time,
                                               combined_commissioning_expected_start_time=combined_commissioning_expected_start_time,
                                               combined_commissioning_expected_completion_time=combined_commissioning_expected_completion_time,
                                               expected_measure_time=expected_measure_time,tester=tester,test_expected_start_time=test_expected_start_time,
                                               test_expected_completion_time=test_expected_completion_time,event_id=event_id,
                                               write_cases=write_cases,cases_expected_start_time=cases_expected_start_time,
                                               cases_expected_completion_time=cases_expected_completion_time)
                # 在中间表增加关联关系
                event_list = [Event.objects.get(pk=event_id) for event_id in event_ids]  # 发布会数据对象列表
                # 方式1
                demand.events.add(*event_list)  # 单纯的添加
                # 方式2
                # guest.events.set(event_list)  # 有覆盖的作用

        except Exception as e:
            return render(request, 'demand_add.html', {'error': repr(e)})
    # 保存成功-跳转到嘉宾列表页
    return redirect('/sgin/demand/')

def search_demand(request):
    if request.method == 'POST':
        pro=request.POST['pro']
        print(pro)
        city=request.POST['city']
        print(city)
        # list = BookInfo.objects.filter(id__in=[1, 3, 5])
        demand_list= Demand.objects.all().raw("select * from sgin_demand sd join sgin_version sde on sd.version = sde.version_name and sde.version_name = %s and sde.id in (select sgin_version_events.version_id from sgin_version_events where sgin_version_events.event_id = %s)",[city,pro])
        print('demand_list',demand_list)
        # 获取版本id
        # d = Version.objects.values('id').filter(version_name=city)
        # d = Version.objects.all().filter(version_name=city)
        # demand_list=[]
        # for i in d:
        #     p=i['id']
        #     print('p',i['id'])
        #     demand_list = Demand.objects.values('name').extra(tables=["sgin_version_events"],
        #                                              where=["sgin_version_events.event_id='{}'".format(pro),
        #                                                     "sgin_version_events.version_id='{}'".format(p)])
        #     print('for里面',demand_list)
        # print(demand_list)
        return render(request, 'demand.html', {'demand_list': demand_list})




# 提测
def measure(request,demand_id):
    if request.method == 'GET':
        demand=Demand.objects.get(id=demand_id)
        print('get')
        return render(request, 'measure.html', {'demand': demand})
    if request.method == 'POST':
        demand=Demand.objects.get(id=demand_id)
        demand_name=demand.name
        measure_time=request.POST['measure_time']
        row_status=request.POST['row_status']
        summary=request.POST['summary']
        if row_status=='全部':
            try:
                with transaction.atomic():
                    Demand.objects.filter(id=demand_id).update(state='1', measure_time=measure_time)
                    text1 = '需求：<font color=“warning”>' + demand_name + '</font>，提测了\n'+'提测范围：全部\n' + '提测内容' + summary
                    # SendWeiXinWenZi().post_file(text1)
            except Exception as e:
                return render(request, 'measure.html', {'error': repr(e)})
        if row_status=='部分':
            try:
                with transaction.atomic():
                    Demand.objects.filter(id=demand_id).update(state='0', measure_time=measure_time)
                    text1 = '需求：<font color=“warning”>' + demand_name + '</font>，提测了\n' + '提测范围：部分\n' + '提测内容：\n' + summary
                    # SendWeiXinWenZi().post_file(text1)
            except Exception as e:
                return render(request, 'measure.html', {'error': repr(e)})

    return redirect('/sgin/demand/')



def single_demand_report(request,demand_id):
    if request.method == 'GET':
        demand = Demand.objects.get(id=demand_id)
        print('get')
        return render(request, 'single_demand_report.html', {'demand': demand})
    if request.method == 'POST':
        tester = request.POST['tester']
        position=request.POST['position']
        time_consuming=request.POST['time_consuming']
        total_cases = request.POST['total_cases']
        executed_cases=request.POST['executed_cases']
        invalid_cases=request.POST['invalid_cases']
        pass_cases=request.POST['pass_cases']
        bug_total = request.POST['bug_total']
        level_1 = request.POST['level_1']
        level_2 = request.POST['level_2']
        level_3 = request.POST['level_3']
        level_4 = request.POST['level_4']
        main_problems = request.POST['main_problems']
        remaining_problems=request.POST['remaining_problems']
        problem_level=request.POST['problem_level']
        problem_types=request.POST['problem_types']
        solutions=request.POST['solutions']
        suggested_optimization = request.POST['suggested_optimization']
        risk = request.POST['risk']
        try:
            with transaction.atomic():
                Demand.objects.filter(id=demand_id).update(pass_cases=pass_cases,position=position,time_consuming=time_consuming,problem_level=problem_level,problem_types=problem_types,solutions=solutions,tester=tester,total_cases=total_cases,executed_cases=executed_cases,invalid_cases=invalid_cases,remaining_problems=remaining_problems,state='2', bug_total=bug_total,level_1=level_1,level_2=level_2,
                                                           level_3=level_3,level_4=level_4,main_problems=main_problems,
                                                           suggested_optimization=suggested_optimization,risk=risk)
        except Exception as e:
            return render(request, 'single_demand_report.html', {'error': repr(e)})

    return redirect('/sgin/demand/')

def single_report_detail(request,demand_id):
    # 获取单个需求报告数据
    try:
        demand = Demand.objects.get(id=demand_id)
    except:
        return render(request, '404.html')

    return render(request, 'single_report_detail.html', {'demand': demand})

# 产品编辑完成信息
def product_revise(request,demand_id):
    if request.method == 'GET':
        demand=Demand.objects.get(id=demand_id)
        return render(request, 'product_revise.html', {'demand': demand})
    if request.method == 'POST':
        prd_actual_start_time=request.POST['prd_actual_start_time']
        prd_actual_completion_time=request.POST['prd_actual_completion_time']
        prd=request.POST['prd']


        try:
            with transaction.atomic():
                Demand.objects.filter(id=demand_id).update(prd_actual_start_time=prd_actual_start_time, prd_actual_completion_time=prd_actual_completion_time,prd=prd)
        except Exception as e:
            return render(request, 'product_revise.html', {'error': repr(e)})

    return redirect('/sgin/demand/')

# 前端完成信息修改
def front_end_completion(request,demand_id):
    if request.method == 'GET':
        demand=Demand.objects.get(id=demand_id)
        return render(request, 'front_end_completion.html', {'demand': demand})
    if request.method == 'POST':
        front_end_actual_start_time=request.POST['front_end_actual_start_time']
        front_end_actual_completion_time=request.POST['front_end_actual_completion_time']

        try:
            with transaction.atomic():
                Demand.objects.filter(id=demand_id).update(front_end_actual_start_time=front_end_actual_start_time, front_end_actual_completion_time=front_end_actual_completion_time)
        except Exception as e:
            return render(request, 'front_end_completion.html', {'error': repr(e)})

    return redirect('/sgin/demand/')

# 后端完成信息修改
def backend_completion(request,demand_id):
    if request.method == 'GET':
        demand=Demand.objects.get(id=demand_id)
        return render(request, 'backend_completion.html', {'demand': demand})
    if request.method == 'POST':
        backend_actual_start_time=request.POST['backend_actual_start_time']
        backend_actual_completion_time=request.POST['backend_actual_completion_time']

        try:
            with transaction.atomic():
                Demand.objects.filter(id=demand_id).update(backend_actual_start_time=backend_actual_start_time, backend_actual_completion_time=backend_actual_completion_time)
        except Exception as e:
            return render(request, 'backend_completion.html', {'error': repr(e)})

    return redirect('/sgin/demand/')

# 联调完成信息修改
def combined_commissioning_completion(request,demand_id):
    if request.method == 'GET':
        demand=Demand.objects.get(id=demand_id)
        return render(request, 'combined_commissioning_completion.html', {'demand': demand})
    if request.method == 'POST':
        combined_commissioning_actual_start_time=request.POST['combined_commissioning_actual_start_time']
        combined_commissioning_actual_completion_time=request.POST['combined_commissioning_actual_completion_time']

        try:
            with transaction.atomic():
                Demand.objects.filter(id=demand_id).update(combined_commissioning_actual_start_time=combined_commissioning_actual_start_time, combined_commissioning_actual_completion_time=combined_commissioning_actual_completion_time)
        except Exception as e:
            return render(request, 'combined_commissioning_completion.html', {'error': repr(e)})

    return redirect('/sgin/demand/')

# 测试完成信息修改
def test_completion(request,demand_id):
    if request.method == 'GET':
        demand=Demand.objects.get(id=demand_id)
        return render(request, 'test_completion.html', {'demand': demand})
    if request.method == 'POST':
        cases_actual_start_time=request.POST['cases_actual_start_time']
        cases_actual_completion_time=request.POST['cases_actual_completion_time']
        test_actual_start_time = request.POST['test_actual_start_time']
        test_actual_completion_time = request.POST['test_actual_completion_time']


        try:
            with transaction.atomic():
                Demand.objects.filter(id=demand_id).update(cases_actual_start_time=cases_actual_start_time, cases_actual_completion_time=cases_actual_completion_time,
                                                           test_actual_start_time=test_actual_start_time,test_actual_completion_time=test_actual_completion_time)
        except Exception as e:
            return render(request, 'test_completion.html', {'error': repr(e)})

    return redirect('/sgin/demand/')



def test_multi_select(request):
    return render(request,'demand.html')

# def get_pro(request):
#     # 获取所有的省级的地名
#     # 返回给前端
#     # return HttpResponse("ok9869869")
#     # 获取所有的省级地名
#     pro_list = City.objects.filter(pid_id__isnull=True)
#     # [<>,<>]
#     # 返回给前端
#     pro_container = []
#     for pro in pro_list:
#         pro_tuple = (pro.id,pro.name)
#         pro_container.append(pro_tuple)
#     res = {"d":pro_container}
#     # import json
#     # pro_json = json.dumps(res,ensure_ascii=False)
#     # return HttpResponse(pro_json)
#     return JsonResponse(res)

def get_pro(request):
    # 获取所有的省级的地名
    # 返回给前端
    # return HttpResponse("ok9869869")
    # 获取所有的省级地名
    pro_list = Event.objects.all()
    # [<>,<>]
    # 返回给前端
    pro_container = []
    for pro in pro_list:
        pro_tuple = (pro.id,pro.name)
        pro_container.append(pro_tuple)
    res = {"d":pro_container}
    # import json
    # pro_json = json.dumps(res,ensure_ascii=False)
    # return HttpResponse(pro_json)
    return JsonResponse(res)

# def get_city(request,pid):
#     pro=City.objects.get(id=pid)
#     city_list=pro.city_set.all()
#     city_container=[(i.id,i.name) for i in city_list]
#     res={"d":city_container}
#
#     return HttpResponse(res)

def get_city(request,pro_id):
    version_list=Version.objects.all().extra(tables=["sgin_version_events"],where=["sgin_version_events.version_id = sgin_version.id","sgin_version_events.event_id='{}'".format(pro_id)])
    # version_list=VersionEvent.objects.filter(event_id=pro_id).version.version_name
    print(version_list)
    version_container=[i.version_name for i in version_list]
    print(version_container)
    res={'d':version_container}
    print(res)
    return JsonResponse(res)
    # return render(request,'demand.html',{'data':version_list})


def add_report_page(request):
    return render(request,'report_add.html')

#版本报告页面
def report(request):
    # 从数据库获取版本报告数据
    report_l = Report.objects.all()
    paginator = Paginator(report_l, 10)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            report_list = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            report_list = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            report_list = paginator.page(paginator.num_pages)
        # 返回模板页面展示版本报告数据
        return render(request,'report.html',{'report_list':report_list})

def add_report(request):
    if request.method == 'GET':
        event_list = Event.objects.all()
        return render(request,'report_add.html',{'events':event_list})
    #获取发布会数据
    if request.method == 'POST':
        report_name = request.POST['report_name']
        event_id = request.POST['pro']
        # event_name = Event.objects.all().raw('select sgin_event.name from sgin_event where sgin_event.id=%s',[event_name_id])
        # print(event_name)
        version_name = request.POST['city']
        test_range = request.POST['test_range']
        model_configuration=request.POST['model_configuration']
        ip_address=request.POST['ip_address']
        operating_system=request.POST['operating_system']
        instructions=request.POST['instructions']
        software_version=request.POST['software_version']
        estimated_space=request.POST['estimated_space']
        testing_tool=request.POST['testing_tool']
        assessment_result=request.POST['assessment_result']
        risk_analysis=request.POST['risk_analysis']
        test_conclusion=request.POST['test_conclusion']

        #创建发布会
        try:
            report = Report.objects.create(report_name=report_name,event_id=event_id,operating_system=operating_system,
                                         version_name=version_name,test_range=test_range,instructions=instructions,
                                         model_configuration=model_configuration,ip_address=ip_address,software_version=software_version,
                                         assessment_result=assessment_result,risk_analysis=risk_analysis,estimated_space=estimated_space,
                                         test_conclusion=test_conclusion,testing_tool=testing_tool)
        except Exception as e:
            return render(request,'report_add.html',{'error':repr(e)}) # repr获取异常的精简信息

        #保存成功
        return redirect('/sgin/report/')

def report_detail(request,report_id):
    # 从某处获取到当前页面的发布会数据对象
    try:
        report = Report.objects.get(id=report_id)
        demand = Demand.objects.all().raw("select * from sgin_report join sgin_demand where sgin_report.event_id=sgin_demand.event_id and sgin_report.version_name=sgin_demand.version and sgin_report.id=%s",[report_id])
        print(demand.query)
        event_name = Event.objects.all().raw("select * from sgin_report as a join sgin_event as b where a.event_id=b.id and a.id=%s",[report_id])
        print(event_name.query)
    except:
        return render(request,'404.html')

    return render(request,'report_detail.html',{'report':report,'demand':demand,'event_name':event_name,})



# # 上传文件
# def upload(request):
#     if request.method == 'GET':
#         return render(request,'demand_detail.html')
#     elif request.method == 'POST':
#         obj = request.FILES.get('fafafa')
#         f = open(os.path.join('sgin/upload',obj.name),'wb')
#         for line in obj.chunks():
#             f.write(line)
#         f.close()
#         return HttpResponse('上传成功')


def index_view(request,demand_id):
    """
    上传文件
    :param request:
    :return:
    """
    if request.method == 'GET':
        demand = Demand.objects.get(id=demand_id)
        print('get')
        return render(request, 'demand_detail.html', {'demand': demand})
    if request.method == 'POST':
        obj = request.FILES.get('fafafa')
        file_id = demand_id
        Demand.objects.filter(id=demand_id).update(file_id=file_id, file_name=obj.name,
                                                   path=os.path.join('sgin/upload', obj.name))

        f = open(os.path.join('sgin/upload', obj.name), 'wb')
        for line in obj.chunks():
            f.write(line)
        f.close()
        return HttpResponse('上传成功')
    else:
        form = FileForm()
        return render(request, 'demand_detail.html', locals())


def download_file(request,demand_id):
    files = Demand.objects.get(id=demand_id)
    # context = {}
    # context['files'] = files

    return render(request,'demand_detail.html',{'files': files})

def download_view(request,file_id):
    """
    下载文件
    :param request:
    :param id:文件id
    :return:
    """
    file_result = Demand.objects.filter(id=file_id)

    print(file_result)
    print(type(file_result))

    # 如果文件存在，就下载文件
    if file_result:

        file = list(file_result)[0]
        # file = file_result

        # 文件名称及路径
        name = file.file_name
        path = file.path

        # 读取文件
        file = open(path, 'rb')
        response = FileResponse(file)

        # 使用urlquote对文件名称进行编码
        response['Content-Disposition'] = 'attachment;filename="' + str(name) + '"'

        return response
    else:
        return HttpResponse('文件不存在!')


def home(request):
    event_list=Event.objects.all()
    # data=[7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
    # 柱状图的数据
    # datas = [{name,data}]

    # return JsonResponse(event_list)
    return render(request, 'home.html', {'event_list': event_list})





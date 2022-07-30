from django.db import models

# Create your models here.

# 发布会模型--需要继承django自带的模型基类
class Event(models.Model):
    # 名称--字符串 最大长度256
    name = models.CharField(max_length=256,null=False)

    summary = models.CharField(max_length=1000,null=False)
    environment = models.CharField(max_length=1000,null=False)
    # 地点
    address = models.CharField(max_length=256)
    # 人数
    limits = models.IntegerField(default=100)
    # 状态
    status = models.BooleanField(default=True)
    # 开始时间--允许为空
    start_time = models.DateTimeField(auto_now_add=True)
    # 一对多
    # version=models.ForeignKey(to='Version',on_delete=models.CASCADE)
    # 多对多
    # demand = models.ForeignKey(to='Demand',on_delete=models.CASCADE)

    # 覆盖对象对外的字符串表现形式
    def __str__(self):
        return self.name

#嘉宾
class Guest(models.Model):
    #关联发布会,外键字段定义在多方
    #event = models.ForeignKey(Event,on_delete=models.CASCADE) #如果删除了该发布会，关联的嘉宾也会被删除
    # 由多对一改成多对多
    events = models.ManyToManyField(Event,through='GuestEvent') # 如果定义了中间表需要手动指定
    # 姓名 唯一 最大长度64
    name = models.CharField(max_length=64,unique=True)
    # 手机号 长度11 唯一
    phone = models.CharField(max_length=11,unique=True)
    # 邮箱 -- 邮箱格式xx@yy.zz
    email = models.EmailField()

    def __str__(self):
        return self.name


class Demand(models.Model):
    # 关联发布会,外键字段定义在多方
    # event = models.ForeignKey(Event,on_delete=models.CASCADE) #如果删除了该发布会，关联的嘉宾也会被删除
    # 由多对一改成多对多
    events = models.ManyToManyField(Event, through='DemandEvent')  # 如果定义了中间表需要手动指定
    # 项目id
    event_id = models.CharField(max_length=20,null=False)
    # 版本
    version = models.CharField(max_length=64,null=False)
    # 需求状态
    state = models.CharField(max_length=20,null=False)
    # 优先级
    priority =models.CharField(max_length=20,null=False)
    # 姓名 唯一 最大长度64
    name = models.CharField(max_length=256, unique=True)
    # 产品经理
    product_manager=models.CharField(max_length=20,null=False)
    # 内容描述
    describe = models.CharField(max_length=600, null=True)
    # prd预期开始时间
    prd_expected_start_time=models.DateTimeField(null=True, blank=True,)
    # ped实际开始时间
    prd_actual_start_time = models.DateTimeField(null=True, blank=True,)
    # 预期完成时间
    prd_expected_completion_time = models.DateTimeField(null=True, blank=True,)
    # 实际完成时间
    prd_actual_completion_time = models.DateTimeField(null=True, blank=True,)

    # PRD及原型地址
    prd = models.CharField(max_length=256,null=True)
    # 前端开发人员
    front_end_developer = models.CharField(max_length=20,null=True)
    # 前端预期开始时间
    front_end_expected_start_time = models.DateTimeField(null=True, blank=True,)
    # 前端实际开始时间
    front_end_actual_start_time = models.DateTimeField(null=True, blank=True,)
    # 前端预期结束时间
    front_end_expected_completion_time = models.DateTimeField(null=True, blank=True,)
    # 前端实际结束数据
    front_end_actual_completion_time = models.DateTimeField(null=True, blank=True,)
    # 后端开发人员
    backend_developers = models.CharField(max_length=20,null=True)
    # 后端预期开始时间
    backend_expected_start_time = models.DateTimeField(null=True, blank=True,)
    # 后端实际开始时间
    backend_actual_start_time = models.DateTimeField(null=True, blank=True,)
    # 后端预期结束时间
    backend_expected_completion_time = models.DateTimeField(null=True, blank=True,)
    # 后端实际结束时间
    backend_actual_completion_time = models.DateTimeField(null=True, blank=True,)
    # 预期联调开始时间
    combined_commissioning_expected_start_time = models.DateTimeField(null=True, blank=True,)
    # 实际联调开始实际
    combined_commissioning_actual_start_time = models.DateTimeField(null=True, blank=True,)
    # 预期联调结束时间
    combined_commissioning_expected_completion_time = models.DateTimeField(null=True, blank=True,)
    # 实际联调结束时间
    combined_commissioning_actual_completion_time = models.DateTimeField(null=True, blank=True,)
    # 预期提测时间
    expected_measure_time = models.DateTimeField(null=True, blank=True,)
    # 实际提测时间
    measure_time = models.DateTimeField(null=True, blank=True,)

    # 用例编写人员
    write_cases=models.CharField(max_length=256,null=True)
    # 用例预期开始时间
    cases_expected_start_time = models.DateTimeField(null=True, blank=True, )
    # 用例实际开始时间
    cases_actual_start_time = models.DateTimeField(null=True, blank=True, )
    # 用例预期结束时间
    cases_expected_completion_time = models.DateTimeField(null=True, blank=True, )
    # 用例实际结束时间
    cases_actual_completion_time = models.DateTimeField(null=True, blank=True, )


    # 预期测试开始时间
    test_expected_start_time = models.DateTimeField(null=True, blank=True,)
    # 实际测试开始时间
    test_actual_start_time = models.DateTimeField(null=True, blank=True,)
    # 预期测试结束时间
    test_expected_completion_time = models.DateTimeField(null=True, blank=True,)
    # 实际测试结束实际
    test_actual_completion_time = models.DateTimeField(null=True, blank=True,)
    # 测试人员
    tester = models.CharField(max_length=256,null=True)
    # 职位
    position= models.CharField(max_length=256, null=True)
    # 耗时
    time_consuming= models.CharField(max_length=256, null=True)
    # 用例总数
    total_cases= models.CharField(max_length=256, null=True)
    # 已执行用例数
    executed_cases= models.CharField(max_length=256, null=True)
    # 用例无效数
    invalid_cases = models.CharField(max_length=256, null=True)
    # 用例通过数
    pass_cases= models.CharField(max_length=256, null=True)
    # 总数
    bug_total = models.CharField(max_length=256,null=True)
    # 一级
    level_1 = models.CharField(max_length=256,null=True)
    # 二级
    level_2 = models.CharField(max_length=256,null=True)
    # 三级
    level_3 = models.CharField(max_length=256,null=True)
    # 四级
    level_4 = models.CharField(max_length=256,null=True)
    # 出现bug的主要问题
    main_problems = models.CharField(max_length=1000,null=True)
    # 优化
    suggested_optimization = models.CharField(max_length=256, null=True)
    # 遗留问题
    remaining_problems= models.CharField(max_length=1000, null=True)
    # 问题等级
    problem_level= models.CharField(max_length=1000, null=True)
    # 问题类型
    problem_types= models.CharField(max_length=1000, null=True)
    # 解决对策
    solutions= models.CharField(max_length=1000, null=True)
    # 风险
    risk = models.CharField(max_length=256,null=True)

    file_id=models.CharField(max_length=50)

    # 文件名称
    file_name = models.CharField(max_length=50)

    # 文件保存路径
    path = models.CharField(max_length=100)


    def __str__(self):
        return self.name

#定义一个中间表
class GuestEvent(models.Model):
    # 通过外键关联对应的数据
    # 当关联的发布会或者嘉宾任意一个被删除，这条对应 关系也就不存在了
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest,on_delete=models.CASCADE)
    # 加入时间 -- 自动获取创建嘉宾数据的时间
    join_time = models.DateTimeField(auto_now_add=True) # auto_now_add 创建的适合自动获取当前时间
    # 签到状态
    is_sgin = models.BooleanField(default=False)

    #修改下表名
    class Meta:  #元类，用于设置模型元信息：表名...
        db_table = 'sgin_guest_events'

#定义一个中间表
class DemandEvent(models.Model):
    # 通过外键关联对应的数据
    # 当关联的发布会或者嘉宾任意一个被删除，这条对应 关系也就不存在了
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    demand = models.ForeignKey(Demand,on_delete=models.CASCADE)
    # 加入时间 -- 自动获取创建嘉宾数据的时间
    join_time = models.DateTimeField(auto_now_add=True) # auto_now_add 创建的适合自动获取当前时间

    # #修改下表名
    class Meta:  #元类，用于设置模型元信息：表名...
        db_table = 'sgin_demand_events'

class City(models.Model):
    name = models.CharField(max_length=20)
    pid = models.ForeignKey("self", on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.name

class Version(models.Model):
    events = models.ManyToManyField(Event, through='VersionEvent')  # 如果定义了中间表需要手动指定
    version_name = models.CharField(max_length=20)

    def __str__(self):
        return self.version_name

#定义一个中间表
class VersionEvent(models.Model):
    # 通过外键关联对应的数据
    # 当关联的发布会或者嘉宾任意一个被删除，这条对应 关系也就不存在了
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    version = models.ForeignKey(Version,on_delete=models.CASCADE)
    # 加入时间 -- 自动获取创建嘉宾数据的时间
    join_time = models.DateTimeField(auto_now_add=True) # auto_now_add 创建的适合自动获取当前时间

    #修改下表名
    class Meta:  #元类，用于设置模型元信息：表名...
        db_table = 'sgin_version_events'

class Report(models.Model):
    # 报告名称
    report_name=models.CharField(max_length=256)
    # 项目名称
    event_id=models.CharField(max_length=256,null=True)
    # 版本号
    version_name=models.CharField(max_length=20,null=True)
    # 测试范围
    test_range=models.CharField(max_length=1000,null=True)
    # 机型（配置）
    model_configuration=models.CharField(max_length=1000)
    # ip地址
    ip_address=models.CharField(max_length=1000)
    # 操作系统
    operating_system=models.CharField(max_length=1000)
    # 用途及特殊说明
    instructions=models.CharField(max_length=1000)
    # 软件及版本
    software_version=models.CharField(max_length=1000)
    # 预计空间
    estimated_space=models.CharField(max_length=1000)
    # 测试工具
    testing_tool=models.CharField(max_length=1000)
    # 评估结果
    assessment_result=models.CharField(max_length=1000,null=True)
    # 质量风险分析
    risk_analysis=models.CharField(max_length=1000,null=True)
    # 测试结论
    test_conclusion=models.CharField(max_length=1000,null=True)
    def __str__(self):
        return self.report_name







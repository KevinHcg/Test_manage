# coding=gbk
# 创建一波省级城市，省级城市的父id为空
def create_data(request):
    """ 临时创建数据用途 """
    from sgin import models
    chars = "断华江辉银市宝剑大地闪石王座绢母环蒸汽江云母峰峦蓝铜沙漠镁铁之森镁铁断层冬青天空透石堡断华裂口山下镇辉锑领铜蓝荒野锂辉峰峦灼热沼泽琥珀平原蓝铜裂口征服天空重盾深潭灼热河众箭村石榴湖泊幽灵沼泽阴暗镇蛇矛沙海剑矛沙海银泉深潭锂云山谷晦暗雨林不眠之地东辉带萤石村蛇矛裂口蒸汽沙漠卑微深潭白骨之地镜海之地绿帘湖泊天之荒野蓝宝石领阴暗雨林灰烬断层重盾陨落地冬泉之森碧空天空辉银天空辉银裂口埋骨海火刃祭坛元素之痕古树泥潭石槌王座刀塔崖海加尔海林边石日泉城高原王座沼光浮岛铁炉山谷索尔森灯塔亚考兰灯塔哈尔什郡碧玉空地刀塔湖佐拉姆洛克提尔谷地冬泉之脊北方水库凄凉湖迷雾哨塔塞拉摩王国雷斧圣殿古树之痕狂风林地奥特兰克城堡法迪尔农场尼加尔的之手阿尔科隆堡垒荒芜群岛坠星之痕悲伤岛提瑞斯法林地西部荒野前哨站法力王座火翼矿洞闪金海葬影谷幽暗之桥乌鸦营地来瑟罗前哨站暗礁矿洞铸魔圣殿西部丘陵激流神庙避难小径暮色环型山环礁森林日蚀峰铁炉神殿"
    import random

    for i in range(1, 11):
        # 随机生成地名
        char_list = random.sample(chars, random.randint(2, 5))
        area_name = "".join(char_list)
        # 保存地名
        obj = models.City.objects.create(name=area_name)
        print(obj)
    return HttpResponse("数据创建成功")

# 创建数据-市级城市
def create_data(request):
    """ 临时创建数据用途 """
    from sgin import models
    chars = "断华江辉银市宝剑大地闪石王座绢母环蒸汽江云母峰峦蓝铜沙漠镁铁之森镁铁断层冬青天空透石堡断华裂口山下镇辉锑领铜蓝荒野锂辉峰峦灼热沼泽琥珀平原蓝铜裂口征服天空重盾深潭灼热河众箭村石榴湖泊幽灵沼泽阴暗镇蛇矛沙海剑矛沙海银泉深潭锂云山谷晦暗雨林不眠之地东辉带萤石村蛇矛裂口蒸汽沙漠卑微深潭白骨之地镜海之地绿帘湖泊天之荒野蓝宝石领阴暗雨林灰烬断层重盾陨落地冬泉之森碧空天空辉银天空辉银裂口埋骨海火刃祭坛元素之痕古树泥潭石槌王座刀塔崖海加尔海林边石日泉城高原王座沼光浮岛铁炉山谷索尔森灯塔亚考兰灯塔哈尔什郡碧玉空地刀塔湖佐拉姆洛克提尔谷地冬泉之脊北方水库凄凉湖迷雾哨塔塞拉摩王国雷斧圣殿古树之痕狂风林地奥特兰克城堡法迪尔农场尼加尔的之手阿尔科隆堡垒荒芜群岛坠星之痕悲伤岛提瑞斯法林地西部荒野前哨站法力王座火翼矿洞闪金海葬影谷幽暗之桥乌鸦营地来瑟罗前哨站暗礁矿洞铸魔圣殿西部丘陵激流神庙避难小径暮色环型山环礁森林日蚀峰铁炉神殿"
    import random

    all_city = ""
    for i in range(1, 30):
        # 随机生成地名
        char_list = random.sample(chars, random.randint(2, 4))
        area_name = "".join(char_list)
        # 保存地名
        obj = models.City.objects.create(name=area_name, pid_id=random.randint(1, 10))
        all_city += "<p>{}</p>".format(obj.name)
    return HttpResponse(all_city)
# 创建数据-区级
def create_data(request):
    """ 临时创建数据用途 """
    from sgin import models
    chars = "断华江辉银市宝剑大地闪石王座绢母环蒸汽江云母峰峦蓝铜沙漠镁铁之森镁铁断层冬青天空透石堡断华裂口山下镇辉锑领铜蓝荒野锂辉峰峦灼热沼泽琥珀平原蓝铜裂口征服天空重盾深潭灼热河众箭村石榴湖泊幽灵沼泽阴暗镇蛇矛沙海剑矛沙海银泉深潭锂云山谷晦暗雨林不眠之地东辉带萤石村蛇矛裂口蒸汽沙漠卑微深潭白骨之地镜海之地绿帘湖泊天之荒野蓝宝石领阴暗雨林灰烬断层重盾陨落地冬泉之森碧空天空辉银天空辉银裂口埋骨海火刃祭坛元素之痕古树泥潭石槌王座刀塔崖海加尔海林边石日泉城高原王座沼光浮岛铁炉山谷索尔森灯塔亚考兰灯塔哈尔什郡碧玉空地刀塔湖佐拉姆洛克提尔谷地冬泉之脊北方水库凄凉湖迷雾哨塔塞拉摩王国雷斧圣殿古树之痕狂风林地奥特兰克城堡法迪尔农场尼加尔的之手阿尔科隆堡垒荒芜群岛坠星之痕悲伤岛提瑞斯法林地西部荒野前哨站法力王座火翼矿洞闪金海葬影谷幽暗之桥乌鸦营地来瑟罗前哨站暗礁矿洞铸魔圣殿西部丘陵激流神庙避难小径暮色环型山环礁森林日蚀峰铁炉神殿"
    import random

    all_city = ""
    for i in range(1, 101):
        # 随机生成地名
        char_list = random.sample(chars, random.randint(2, 4))
        area_name = "".join(char_list)
        # 保存地名
        obj = models.City.objects.create(name=area_name, pid_id=random.randint(11,39))
        all_city += "<p>{}-{}</p>".format(obj.id, obj.name)
        #
    return HttpResponse(all_city)
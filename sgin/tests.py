from django.test import TestCase

# Create your tests here.
# 发布会模型测试
from sgin.models import Event,Guest
from datetime import datetime

class EventTestCase(TestCase):
    def setUp(self) -> None:
        #准备发布会数据
        Event.objects.create(name='测试训练营1',address='花神大道',limits=500,start_time=datetime.now())
        Event.objects.create(name='测试训练营2',address='花神大道',limits=100,start_time=datetime.now())

    def test_event_address(self):
        event1 = Event.objects.get(name='测试训练营1')
        event2 = Event.objects.get(name='测试训练营2')
        assert event1.address == '花神大道'
        assert event2.address == '花神大道'

    def test_event_limits(self):
        event1 = Event.objects.get(name='测试训练营1')
        event2 = Event.objects.get(name='测试训练营2')
        assert event1.limits == 500
        assert event2.limits == 100


# 嘉宾测试c
class GuestTestCase(TestCase):
    def setUp(self) -> None:
        event1 = Event.objects.create(name='测试训练营1',address='花神大道',limits=500,start_time=datetime.now())
        event2 = Event.objects.create(name='测试训练营1',address='花神大道',limits=500,start_time=datetime.now())

        guset = Guest.objects.create(name='小杨',phone='13925685956',email='xiaoyang@testdev.com',)
        #关联
        guset.events.add(event1,event2)

    def test_update(self):
        guest = Guest.objects.get(phone='13925685956')
        guest.name = '小张'
        guest.save() #保存更改
        guest2 =Guest.objects.get(phone='13925685956')
        assert guest.name == guest2.name

    def test_delete(self):
        guest = Guest.objects.get(phone='13925685956')
        # 删除
        guest.delete()
        guest_list = Guest.objects.all()
        assert guest not in guest_list

    def test_query_multiply(self):
        guest = Guest.objects.get(phone='13925685956')
        # print(guest.events.all())
        event1 = Event.objects.get(name='测试训练营1')
        #反向查询  数据对象.多方模型小写_set.all().filter().get()

        print(event1.guest_set.all())
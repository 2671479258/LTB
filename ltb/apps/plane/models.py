from django.db import models
from users.models import User
# Create your models here.

class Plane_Company(models.Model):
    name=models.CharField(max_length=20)
    logo=models.CharField(max_length=150)

    class Meta:
        app_label = 'plane'
        db_table='plane_company'
        verbose_name='航空公司管理'
        verbose_name_plural=verbose_name


class Plane_Name(models.Model):
    name=models.CharField(max_length=20)
    company=models.ForeignKey(Plane_Company,on_delete=models.CASCADE, verbose_name='所属公司')

    class Meta:
        app_label = 'plane'
        db_table='plane_name'
        verbose_name='飞机管理'
        verbose_name_plural=verbose_name

class Flight(models.Model):
    plane=models.ForeignKey(Plane_Name,on_delete=models.CASCADE, verbose_name='飞机名字')
    departureCity=models.CharField(max_length=20)
    destinationCity=models.CharField(max_length=20)
    departureDate = models.DateField()
    start_time=models.CharField(max_length=20,null=True)
    arrive_time=models.CharField(max_length=20,null=True)
    start_place = models.CharField(max_length=20, null=True)
    arrive_place = models.CharField(max_length=20, null=True)
    price=models.CharField(max_length=20, null=True)

    class Meta:
        app_label = 'plane'
        db_table='tb_flight'
        verbose_name='航班管理'
        verbose_name_plural=verbose_name

class Flight_Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    flight=models.ForeignKey(Flight,on_delete=models.CASCADE,verbose_name='航班')
    passenger_name = models.CharField(max_length=100, verbose_name='乘客姓名')
    passenger_gender = models.CharField(max_length=10, choices=[('male', '男性'), ('female', '女性')], verbose_name='乘客性别')
    passenger_phone = models.CharField(max_length=11, verbose_name='乘客手机号')
    passenger_id = models.CharField(max_length=18, verbose_name='身份证号')


    class Meta:
        app_label='plane'
        db_table='flight_order'
        verbose_name = '航班订单'
        verbose_name_plural = '航班订单'



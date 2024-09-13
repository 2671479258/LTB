from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # 使用 set_password 来设置密码的哈希值
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15, unique=True)
    mobile = models.CharField(max_length=11, unique=True, null=True)
    profile = models.CharField(max_length=200, default='http://127.0.0.1:8080/images/profile/default.jpg')
    email = models.EmailField(max_length=255, unique=True, null=True)
    bio = models.TextField(blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # 其他必需字段

    def __str__(self):
        return self.username



class Hotel(models.Model):
    city=models.CharField(max_length=50,default='未知地')
    name = models.CharField(max_length=255)  # 酒店名称
    description = models.TextField()  # 酒店描述
    location = models.CharField(max_length=255)  # 地点
    distance_to_city_center = models.DecimalField(max_digits=5, decimal_places=2)  # 距离市中心的距离
    review_count = models.IntegerField()  # 评分数量
    rating = models.DecimalField(max_digits=3, decimal_places=2)  # 评分
    hotel_img = models.CharField(max_length=200, default='http://127.0.0.1:8080/images/hotel/default.jpg')
    level=models.CharField(max_length=6,null=True,default='未知')
    detail_location=models.CharField(max_length=255,null=True)  # 地点


    def __str__(self):
        return self.name


class Roomtype(models.Model):
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE, verbose_name='所属酒店')
    name = models.CharField(max_length=100)  # 房型名称
    description = models.TextField()  # 房型描述
    size =models.CharField(max_length=200,null=True)  # 房间大小，单位可以是平方米
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 房型价格
    has_window = models.BooleanField(default=False)  # 有无窗户
    has_breakfast = models.BooleanField(default=False)  # 有无早餐
    room_img = models.CharField(max_length=200, default='http://127.0.0.1:8080/images/room/default.jpg')
    room_capacity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.name


from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)  # 城市名字的最大长度为100个字符

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'users'
        db_table='tb_citys'
        verbose_name='城市列表'
        verbose_name_plural=verbose_name
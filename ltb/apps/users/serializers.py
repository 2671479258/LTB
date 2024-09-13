from django.db.models import Min
from rest_framework import serializers
from users.models import Hotel, User, Roomtype


class HotelModelSerializers(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    url = serializers.SerializerMethodField()  # 添加一个额外的字段来包含 url 属性
    min_price = serializers.SerializerMethodField()  # 添加一个额外的字段来包含最小价格

    class Meta:
        model = Hotel
        fields = "__all__"

    def get_url(self, obj):
        # 根据每个酒店对象的 id 生成对应的 URL
        return 'http://127.0.0.1:8080/hotels/' + str(obj.id) + '.html'

    def get_min_price(self, obj):
        # 查询该酒店的所有房间价格，并返回最小值
        min_price = Roomtype.objects.filter(hotel=obj).aggregate(min_price=Min('price'))['min_price']
        return min_price if min_price else 0

class UserModelSerializers(serializers.ModelSerializer):   #继承ModelSerializer

    class Meta:
        model = User
        fields = ('mobile', 'profile','email','bio')  # 指定要序列化的字段
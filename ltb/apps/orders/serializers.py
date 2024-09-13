from rest_framework import serializers
from hotels.models import Hotel_Order

class HotelOrderModelSerializers(serializers.ModelSerializer):   #继承ModelSerializer
    nickname=serializers.CharField(read_only=True)
    class Meta:
        model = Hotel_Order
        fields = "__all__"

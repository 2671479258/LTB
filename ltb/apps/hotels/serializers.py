from rest_framework import serializers
from users.models import City


class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


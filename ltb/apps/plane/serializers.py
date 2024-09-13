from django.db.models import Min
from rest_framework import serializers
from plane.models import Flight,Plane_Company,Plane_Name,Flight_Order

class PlaneCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane_Company
        fields = ['name', 'logo']

class PlaneNameSerializer(serializers.ModelSerializer):
    company = PlaneCompanySerializer()

    class Meta:
        model = Plane_Name
        fields = ['name', 'company']

class FlightModelSerializers(serializers.ModelSerializer):   #继承ModelSerializer

    class Meta:
        model = Flight
        fields = "__all__"


class FlightOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model=Flight_Order
        fields="__all__"
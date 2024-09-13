from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from plane.models import Flight,Flight_Order
from .serializers import FlightModelSerializers,FlightOrderSerializers


class SearchPlane(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Flight.objects.all()
    serializer_class = FlightModelSerializers

    def post(self, request, *args, **kwargs):
        data = request.data
        departureCity = data.get('departureCity', '')
        destinationCity = data.get('destinationCity', '')
        departureDate = data.get('departureDate', '')

        query = Q()
        if departureCity:
            query &= Q(departureCity=departureCity)
        if destinationCity:
            query &= Q(destinationCity=destinationCity)
        if departureDate:
            query &= Q(departureDate=departureDate)

        # 根据查询条件查询数据库
        flights = Flight.objects.filter(query)

        results = []

        for flight in flights:
            flight_data = {
                'id': flight.id,
                'departureCity': flight.departureCity,
                'destinationCity': flight.destinationCity,
                'departureDate': flight.departureDate,
                'start_time': flight.start_time,
                'arrive_time': flight.arrive_time,
                'start_place': flight.start_place,
                'arrive_place': flight.arrive_place,
                'price': flight.price,
                'plane_number': flight.plane.name,
                'company_name': flight.plane.company.name,
                'logo': flight.plane.company.logo,
            }
            results.append(flight_data)

        return Response({
            'data': results,
            'departureCity': departureCity,
            'destinationCity': destinationCity,
            'departureDate': departureDate
        }, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance)
        data = serializer.data

        # 获取飞机和公司的名称
        plane = instance.plane
        company = plane.company
        logo=plane.company.logo

        # 添加新的字段到返回的数据中
        extra_data = {
            'plane_name': plane.name,
            'company_name': company.name,
            'logo':logo
        }

        data.update(extra_data)

        return Response(data, status=status.HTTP_200_OK)


class flight_order(GenericAPIView, ListModelMixin):
    queryset = Flight_Order.objects.all()
    serializer_class = FlightOrderSerializers
    def post(self, request):
        authentication = JWTAuthentication()
        try:
            # 从请求中获取 token
            raw_token = request.headers.get('Authorization', None)
            if raw_token is None or not raw_token.startswith('Bearer '):
                raise AuthenticationFailed('Token not provided or malformed.')
            token = raw_token.split(' ')[1]

            # 验证 token
            validated_token = authentication.get_validated_token(token)
            user = authentication.get_user(validated_token)
            print(request.data)
            # 打印用户名

            name=request.data['name']
            gender=request.data['gender']
            phone=request.data['phone']
            credit=request.data['credit']
            flight_id=request.data['flight_id']


            flight=Flight.objects.filter(id=flight_id).first()
            if not flight:
                return JsonResponse({'error': 'Flight not found'}, status=404)

            flight_order = Flight_Order(
                user=user,
                flight=flight,
                passenger_name=name,
                passenger_gender=gender,
                passenger_phone=phone,
                passenger_id=credit
            )
            flight_order.save()

            # 返回成功的响应
            return JsonResponse({'message': '成功'}, status=200)

        except AuthenticationFailed as e:
            return JsonResponse({'error': str(e)}, status=401)

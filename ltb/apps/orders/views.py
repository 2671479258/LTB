from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from hotels.models import Hotel_Order
from .serializers import HotelOrderModelSerializers
from plane.serializers import FlightOrderSerializers
from users.models import User,Roomtype

from plane.models import Flight_Order,Flight,Plane_Name,Plane_Company
from rest_framework.pagination import PageNumberPagination

class My_Order(APIView):
    def get(self, request):

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

        except AuthenticationFailed as e:
            return JsonResponse({'error': str(e)}, status=401)

        orders = Hotel_Order.objects.filter(user=user)

        paginator = PageNumberPagination()
        paginator.page_size = 2

        result_page = paginator.paginate_queryset(orders, request)
        serializer = HotelOrderModelSerializers(result_page, many=True)
        print(serializer.data)

        processed_data = []

        for data in serializer.data:
            room_type_id = data['selectedRoom']
            room_type = Roomtype.objects.get(pk=room_type_id)
            hotel_name = room_type.hotel.name
            hotel_area = room_type.hotel.detail_location
            room_name = room_type.name
            data['hotel_name'] = hotel_name
            data['room_name'] = room_name
            data['hotel_area'] = hotel_area
            processed_data.append(data)
        print(processed_data)

        return paginator.get_paginated_response(processed_data)


class My_Flight_Order(APIView):
    def get(self, request):

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

        except AuthenticationFailed as e:
            return JsonResponse({'error': str(e)}, status=401)

        orders = Flight_Order.objects.filter(user=user)

        paginator = PageNumberPagination()
        paginator.page_size = 2

        result_page = paginator.paginate_queryset(orders, request)
        serializer = FlightOrderSerializers(result_page, many=True)
        print(serializer.data)

        processed_data = []
        for data in serializer.data:
            flight_id = data['flight']
            flight=Flight.objects.get(pk=flight_id)
            departureCity=flight.departureCity
            destinationCity=flight.destinationCity
            start_time=flight.start_time
            arrive_time=flight.arrive_time

            plane = Plane_Name.objects.get(pk=flight_id)
            plane_name = plane.name

            company = plane.company
            company_name = company.name

            data['departureCity']=departureCity
            data['destinationCity'] = destinationCity
            data['destinationCity'] = destinationCity
            data['start_time'] = start_time
            data['arrive_time'] = arrive_time
            data['plane_name']=plane_name
            data['company_name']=company_name
            processed_data.append(data)
        print(processed_data)

        return paginator.get_paginated_response(processed_data)

import json
from datetime import datetime

from django.http import JsonResponse
from rest_framework.mixins import ListModelMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from hotels.serializers import CitySerializers

from users.models import Roomtype, Hotel,User,City

from rest_framework.generics import GenericAPIView

class CityList(GenericAPIView, ListModelMixin):
    queryset = City.objects.all()
    serializer_class = CitySerializers

    def get(self,requests):
        return self.list(requests)


def get_room_and_hotel_info(request):
    if request.method == 'POST':
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
        data = json.loads(request.body)
        room_id = data.get('roomId')
        print(room_id)
        try:
            room = Roomtype.objects.get(id=room_id)
            hotel = room.hotel
            response_data = {
                'room': {
                    'name': room.name,
                    'description': room.description,
                    'size': room.size,
                    'price': str(room.price),
                    'has_window': room.has_window,
                    'has_breakfast': room.has_breakfast,
                    'room_img': room.room_img,
                    'room_capacity':room.room_capacity,

                },
                'hotel': {
                    'name': hotel.name,
                    'description': hotel.description,
                    'location': hotel.location,
                    'distance_to_city_center': str(hotel.distance_to_city_center),
                    'review_count': hotel.review_count,
                    'rating': str(hotel.rating),
                    'hotel_img': hotel.hotel_img,
                    'level': hotel.level,
                    'detail_location': hotel.detail_location
                }
            }

            # 打印组合后的数据
            print(response_data)

            # 将数据以 JSON 格式返回给前端
            return JsonResponse(response_data)
        except Roomtype.DoesNotExist:
            return JsonResponse({'error': 'Room not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

from hotels.models import Hotel_Order

class hotel_order(GenericAPIView, ListModelMixin):
    queryset = User.objects.all()
    def post(self, request):
        current_year = datetime.now().year
        username = request.COOKIES.get('username')
        user = self.get_queryset().filter(username=username).first()
        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)
        # 获取表单数据
        check_in_date = request.POST.get('checkInDate')
        check_out_date = request.POST.get('checkOutDate')
        room_count = request.POST.get('roomCount')
        guest_name = request.POST.get('guestName')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        estimated_arrival_time = request.POST.get('estimatedArrivalTime')
        selected_room_id = request.POST.get('selectedRoomId')

        # 验证 selected_room_id
        selected_room = Roomtype.objects.filter(id=selected_room_id).first()
        if not selected_room:
            return JsonResponse({'error': 'Selected room not found'}, status=404)

        # 创建并保存 Hotel_Order 实例
        hotel_order = Hotel_Order(
            user=user,
            selectedRoom=selected_room,
            current_year=current_year,
            checkInDate=check_in_date,
            checkOutDate=check_out_date,
            roomCount=room_count,
            guestName=guest_name,
            email=email,
            phoneNumber=phone_number,
            estimatedArrivalTime=estimated_arrival_time
        )
        hotel_order.save()

        # 返回响应
        response_data = {
            'message': 'Order received successfully',
            'data': {
                'order_number': hotel_order.order_number,
                'user': user.id,
                'current_year': current_year,
                'checkInDate': check_in_date,
                'checkOutDate': check_out_date,
                'roomCount': room_count,
                'guestName': guest_name,
                'email': email,
                'phoneNumber': phone_number,
                'estimatedArrivalTime': estimated_arrival_time,
                'selectedRoomId': selected_room_id
            }
        }
        return JsonResponse(response_data, status=200)
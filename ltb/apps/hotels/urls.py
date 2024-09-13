from django.urls import path
from hotels import views
urlpatterns = [
path('get_room_and_hotel_info/', views.get_room_and_hotel_info, name='get_room_and_hotel_info'),
    path('hotel_order/', views.hotel_order.as_view()),
    path('city_list/',views.CityList.as_view())

]
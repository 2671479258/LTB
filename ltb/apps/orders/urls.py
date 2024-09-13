from django.urls import path, re_path
from orders import views
from orders.views import My_Order,My_Flight_Order

urlpatterns = [
    path('my_orders/', My_Order.as_view()),
    path('my_flight_orders/', My_Flight_Order.as_view()),



]
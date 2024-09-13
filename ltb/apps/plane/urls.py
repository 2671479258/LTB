from django.urls import path
from plane import views
urlpatterns = [

    path('search/', views.SearchPlane.as_view()),
    path('flight_detail/<int:pk>/', views.SearchPlane.as_view()),
    path('flight_order/', views.flight_order.as_view()),

]
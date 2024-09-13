from django.urls import path
from users import views



urlpatterns = [
path('login/',views.LoginView.as_view()),
path('register/',views.RegisterView.as_view()),

    path('get_profile/', views.GetProfile.as_view()),
path("hotel/", views.HotelAPIView.as_view()),
path("get_userinfo/", views.GetUserInfo.as_view()),
path("upload_avatar/", views.UploadAvatar.as_view()),
    path('logout/',views.LogoutView.as_view()),


]
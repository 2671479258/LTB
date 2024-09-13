from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Hotel
from django.http import JsonResponse
import json
from .forms import RegisterForm, LoginForm

from users.serializers import HotelModelSerializers,UserModelSerializers


class RegisterView(View):
    def post(self, request):
        try:

            body_bytes = request.body
            print(body_bytes)
            body_dict = json.loads(body_bytes)
            print(body_dict)
            form = RegisterForm(body_dict)
            if not form.is_valid():
                return JsonResponse({'code': 400, 'errmsg': form.errors})
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            mobile = form.cleaned_data.get('mobile')  # 确保在创建用户时使用了 mobile 字段
            User.objects.create_user(username=username, password=password,mobile=mobile)


            user = authenticate(username=username, password=password)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = JsonResponse({'code': 0, 'errmsg': '注册成功','access': access_token,
            'refresh': refresh_token})

            response.set_cookie('username', username, max_age=3600 * 24 * 15)  # 设置 Cookie
            response.set_cookie('access_token', access_token, max_age=3600 * 24 * 15)
            response.set_cookie('refresh_token', refresh_token, max_age=3600 * 24 * 15)
            return response
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '注册失败'})



class LoginView(View):
    def post(self, request):
        import json
        data = json.loads(request.body)
        form = LoginForm(data)
        if not form.is_valid():
            return JsonResponse({'code': 400, 'errmsg': form.errors})
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})
        # 生成 JWT 令牌
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = JsonResponse({
            'code': 0,
            'errmsg': '登录成功',
            'access': access_token,
            'refresh': refresh_token
        })
        response.set_cookie('username', username, max_age=3600 * 24 * 15)
        response.set_cookie('access_token', access_token, max_age=3600 * 24 * 15)
        response.set_cookie('refresh_token', refresh_token, max_age=3600 * 24 * 15)

        return response



class LogoutView(View):
    def delete(self,request):
        response=JsonResponse({'code':400,'errmsg':'ok'})
        response.delete_cookie('username')
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


class GetProfile(View):
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

        username = request.COOKIES.get('username')


        user = User.objects.filter(username=username).first()
        print(user)
        profile = None
        if user is not None:
            profile = user.profile
            print(profile)


        return JsonResponse({'profile': profile})



from rest_framework.mixins import ListModelMixin
class HotelAPIView(GenericAPIView, ListModelMixin):
    queryset = Hotel.objects.all()
    serializer_class = HotelModelSerializers
    def post(self, request):
        data = request.data
        print(data)
        # 获取目的地和酒店级别
        destination = data.get('destination', '')
        print(destination)
        hotel_level = data.get('hotelLevel', '')
        # 构建查询条件
        query = Q()
        if destination:
            query &= Q(city__icontains=destination)
        if hotel_level and hotel_level != '任意级别':
            query &= Q(level=hotel_level)
        hotels = Hotel.objects.filter(query)
        serializer = self.serializer_class(hotels, many=True)
        print(serializer.data)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class GetUserInfo(GenericAPIView, ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserModelSerializers
    def get(self, request):
        username = request.COOKIES.get('username')
        user = self.get_queryset().filter(username=username).first()
        if user:
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        else:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

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

        except AuthenticationFailed as e:
            return JsonResponse({'error': str(e)}, status=401)

        username = request.COOKIES.get('username')
        user = self.get_queryset().filter(username=username).first()
        print(request.data)
        if user:
            serializer = UserModelSerializers(user, data=request.data)

            if serializer.is_valid():
                serializer.save()
                response = Response(serializer.data)
                return response
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UploadAvatar(APIView):
    def post(self, request):
        if 'avatar' not in request.FILES:
            return Response({'error': 'No file was submitted'}, status=status.HTTP_400_BAD_REQUEST)

        avatar = request.FILES['avatar']
        username = request.COOKIES.get('username')
        print(username)

        # 根据 username 查询用户的 ID
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # 使用用户的 ID 作为文件名
        file_name = str(user.id) + '.jpg'

        # 指定文件保存路径
        file_path = 'D:/python/github/yiliao/LTB/front/images/profile/' + file_name
        with open(file_path, 'wb+') as destination:
            for chunk in avatar.chunks():
                destination.write(chunk)
        profile_url = f'http://127.0.0.1:8080/images/profile/{file_name}'

        # 更新数据库中的用户资料
        user.profile = profile_url
        user.save()
        # 返回保存的文件路径
        return Response({'profile_url': '/images/profile/' + file_name}, status=status.HTTP_201_CREATED)
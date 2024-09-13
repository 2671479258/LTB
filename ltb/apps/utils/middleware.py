# from django.http import JsonResponse
# from users.models import User
#
# class CookieAuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.protected_urls = ['/hotels/get_room_and_hotel_info/','']  # 添加需要身份验证的URL
#
#     def __call__(self, request):
#         # 检查请求是否在需要身份验证的URL列表中
#         if request.path in self.protected_urls:
#             username = request.COOKIES.get('username')
#             print(username)
#             if username:
#                 try:
#                     user = User.objects.get(username=username)
#                     request.user = user
#                 except User.DoesNotExist:
#                     return JsonResponse({'detail': 'Unauthorized'}, status=401)
#             else:
#                 return JsonResponse({'detail': 'Unauthorized'}, status=401)
#
#         # 如果请求路径不需要身份验证，直接继续处理请求
#         response = self.get_response(request)
#         return response
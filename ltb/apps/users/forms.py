from django import forms
from django.core.exceptions import ValidationError
from users.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(
        min_length=4,
        max_length=15,  # 根据你的模型设置 max_length=15
        required=True,
        error_messages={
            'required': '用户名不能为空。',
            'min_length': '用户名必须至少包含4个字符。',
            'max_length': '用户名最多只能包含15个字符。'
        }
    )
    password = forms.CharField(
        min_length=5,
        required=True,
        error_messages={
            'required': '密码不能为空。',
        }
    )
    mobile = forms.CharField(
        min_length=11,
        max_length=11,
        required=True,
        error_messages={
            'required': '手机号不能为空。',
            'max_length': '手机号必须为11个数字',
            'min_length':'手机号必须为11个数字'
        }
    )

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if User.objects.filter(mobile=mobile).exists():
            raise ValidationError('手机号已被注册。')
        return mobile

class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=4,
        max_length=15,
        required=True,
        error_messages={
            'required': '用户名不能为空。',
            'min_length': '用户名必须至少包含4个字符。',
            'max_length': '用户名最多只能包含15个字符。'
        }
    )

    password = forms.CharField(
        min_length=5,
        required=True,
        error_messages={
            'required': '密码不能为空。',
        }
    )


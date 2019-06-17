import re

from django import http
from django.contrib.auth.backends import ModelBackend

from django.shortcuts import render, redirect

# Create your views here.
# from django.urls import reverse
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login

from apps.users.models import User


def get_user_by_account(account):
    try:
        if re.match('^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)

        if user and user.check_password(password):
            return user




class UserLoginView(UsernameMobileAuthBackend, View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 1接收数据，username(mobile )password
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        # 2 判断数据  数据是否齐全  数据是否符合正则条件
        if not all([username, password]):
            return http.HttpResponseBadRequest('参数不齐')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseBadRequest('请输入正确的用户名或手机号')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseBadRequest('密码最少8位，最长20位')

        # 3 校验数据  数据是否正确

        user = authenticate(request, username=username, password=password)
        if user is None:
            return http.HttpResponseBadRequest('请检查数据是否正确')

        # 4 状态保持
        login(request, user)

        if remembered == 'on':
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)


        # 　5 返回数据
        response = redirect(reverse('contents:index'))
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        login(request, user)
        return response

class LoginOut(View):
    def get(self, request):
        logout(request)

        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')
        return response

class UserInfo(View):
    def get(self, request):
        return render(request, 'user_center_info.html')



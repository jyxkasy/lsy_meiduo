from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.users import models
import re
from django import http


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 获取数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')

        # 判断数据
        # 数据是否完整
        if not all([username, password, password2, mobile]):
            return http.HttpResponseBadRequest('参数不齐')
        if not re.match(r'[a-zA-Z0-9_]{5,20}', username):
            return http.HttpResponseBadRequest('姓名不符合要求')
        if not re.match(r'[a-zA-Z0-9_]{8,20}'):
            return http.HttpResponseBadRequest('密码不合法')
        if password != password2:
            return http.HttpResponseBadRequest('两次密码不相同')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseBadRequest('请输入正确的手机号码')

        try:
            count = models.User.objects.create_user(username=username)
        except Exception as e:
            pass

        # 入库

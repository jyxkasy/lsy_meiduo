from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from apps.users.models import User
import re
from django import http
from django.contrib.auth import login
import logging

logger = logging.getLogger('django')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 获取数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')

        # 判断数据
        # 数据是否完整
        if not all([username, password, password2, mobile]):
            return http.HttpResponseBadRequest('参数不齐')
        if not re.match(r'[a-zA-Z0-9_]{5,20}', username):
            return http.HttpResponseBadRequest('姓名不符合要求')
        if not re.match(r'[a-zA-Z0-9_]{8,20}', password):
            return http.HttpResponseBadRequest('密码不合法')
        if password != password2:
            return http.HttpResponseBadRequest('两次密码不相同')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseBadRequest('请输入正确的手机号码')
        if allow != 'on':
            return http.HttpResponseBadRequest('请勾选用户协议')
        # 用户数据入库

        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except Exception as e:

            return render(request, 'register.html', {'register_errmsg': '注册失败'})

            # 错误日志
        return http.HttpResponse('ok')


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


# 校验用户姓名重复
class UsernameCountView(View):

    def get(self, request, username):
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': 400, 'count': count})
        return http.JsonResponse({'code': 0, 'count': count})


# 校验用户电话号码是否重复
class MobileCountView(View):
    def get(self, request, mobile):
        try:
            count = User.objects.filter(mobile=mobile).count()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': 400, 'count': count})
        return http.JsonResponse({'code': 0, 'count': count})


from libs.captcha.captcha import captcha
from django_redis import get_redis_connection


class ImageCode(View):
    def get(self, requset, uuid):
        text, image = captcha.generate_captcha()
        # 链接redis
        redis_conn = get_redis_connection('code')

        # 保存在redis
        redis_conn.setex(uuid, 240, text)
        return http.HttpResponse(image, content_type='image/jpeg')


from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from apps.users.models import User
import re
from django import http
from django.contrib.auth import login
import logging

from libs.yuntongxun.sms import CCP

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
        if not all([username, password, password2, mobile, allow]):
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

        # User.objects.create  直接入库 理论是没问题的 但是 大家会发现 密码是明文
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except Exception as e:
            logger.error(e)
            return render(request, 'register.html', context={'error_message': '数据库异常'})

        from django.contrib.auth import login
        login(request, user)

        return redirect(reverse('contents:contents'))


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
        redis_conn.setex(uuid, 300, text)
        return http.HttpResponse(image, content_type='image/jpeg')


class MobileCode(View):
    def get(self, request, mobile):
        image_code = request.GET.get('image_code').lower()
        image_code_id = request.GET.get('image_code_id')
        # 判断参数是否完整
        if not all([mobile, image_code, image_code_id]):
            return http.JsonResponse({'code': 400, 'errmsg': '参数不完整， 请重新输入'})

        # 接受参数 电话号码 图形验证码 uuid
        # 判断图形验证码是否正确
        # 获取redis中的数据
        try:
            redis_conn = get_redis_connection('code')
            redis_code = redis_conn.get(image_code_id).decode().lower()
        except Exception as e:
            return http.JsonResponse({'code': 400, 'errmsg': 'redis错误'})

        # if redis_code == None:
        #     return http.JsonResponse({'code':400, 'errmsg':'没有图片验证码'})
        from random import randint
        # 创建redis查询合并对象
        pl = redis_conn.pipeline()
        # 判断图形验证码是否正确
        if redis_code != image_code:
            return http.JsonResponse({'code': 400, 'errmsg': '图形验证码不正确'})
        # 判断电话号码是否存在
        redis_count_mobile = redis_conn.get(mobile)
        if redis_count_mobile:
            return http.JsonResponse({'code': '4001', 'errmsg': '操作频繁'})



        # 生成短信验证码
        mobile_code = randint(100000, 999999)
        # 保存短信验证码
        # 创建redis管道
        pl = redis_conn.pipeline()
        # 把redis操作加入缓存
        pl.setex(mobile, 300, mobile_code)
        pl.setex(mobile, 300, 1)
        # 执行缓存中的命领
        pl.execute()

        # 发送短信验证码
        CCP().send_template_sms(mobile, [mobile_code, 5], 1)
        # 保存短信验证码
        return http.JsonResponse({'code': '0'})
        # 防止重复发送验证码

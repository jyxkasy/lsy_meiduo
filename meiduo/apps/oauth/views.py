from django import http
from django.contrib.auth import login
from django.shortcuts import reverse, redirect, render

from QQLoginTool.QQtool import OAuthQQ
# Create your views here.
from django.urls import reverse
from django.views import View
from apps.oauth.models import OAuthQQUser


class QQLogin(View):
    def get(self, request):
        # 数据准备

        QQ_CLIENT_ID = '101518219'

        QQ_CLIENT_SECRET = '418d84ebdc7241efb79536886ae95224'

        QQ_REDIRECT_URI = 'http://www.meiduo.site:8000/oauth_callback'
        # 创建工具对象

        oauth = OAuthQQ(client_id=QQ_CLIENT_ID, client_secret=QQ_CLIENT_SECRET, redirect_uri=QQ_REDIRECT_URI, state=next)
        # 获取跳转的url
        login_url = oauth.get_qq_url()

        return  http.JsonResponse({'login_url':login_url})


class QQAuthUserView(View):
    def get(self, request):
        # 1 获取code
        code = request.GET.get('code')

        if not code:
            return http.HttpResponseBadRequest('没有code')
        # 2创建工具对象
        QQ_CLIENT_ID = '101518219'

        QQ_CLIENT_SECRET = '418d84ebdc7241efb79536886ae95224'

        QQ_REDIRECT_URI = 'http://www.meiduo.site:8000/oauth_callback'

        oauth = OAuthQQ(client_id=QQ_CLIENT_ID, client_secret=QQ_CLIENT_SECRET, redirect_uri=QQ_REDIRECT_URI,
                        state=next)
        try:
            # 3使用code 获取token
            access_token = oauth.get_access_token(code)
            # 4 使用token 获取openid
            openid = oauth.get_open_id(access_token)

        except Exception as e:
            return http.HttpResponseServerError("认证失败")

        # 获取openid
        # 查询
        try:
            openidoauth_user = OAuthQQUser.objects.filter(openid=openid).count()

            if openidoauth_user == 0:
                # 如果openid不存在，返回绑定页面

                return render(request, 'oauth_callback.html')
            else:
                # 如果openid存在，返回绑定页面
                qq_user = openidoauth_user.user
                login(request, qq_user)
                return redirect(reverse('contents:index'))
        except Exception as e:
            return http.HttpResponseBadRequest("数据库错误")

        # 如果openid不存在，返回绑定页面
        # 如果openid存在,状态保持，登录，返回首页

class OpenidCallback(View):
    def get(self, request):
        pass

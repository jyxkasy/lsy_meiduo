from django.conf.urls import url
from apps.oauth import views

urlpatterns = [
    url(r'^qq/login/$', views.QQLogin.as_view(), name='qqoauth'),
    url(r'^oauth_callback/$', views.QQAuthUserView.as_view()),
    url(r'^openid_callback/$', views.OpenidCallback.as_view(), name='openidcallback'),
]
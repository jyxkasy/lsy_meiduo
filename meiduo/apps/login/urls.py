from django.conf.urls import url
from apps.login import views

urlpatterns = [
    url(r'^login/$', views.UserLoginView.as_view(), name='login'),
    url(r'^logout/$', views.LoginOut.as_view(), name='logout'),
    url(r'^usercenterinfo', views.UserInfo.as_view(), name='usercenterinfo')
]

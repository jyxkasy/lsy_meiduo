from django.conf.urls import url
from apps.users import views

urlpatterns = [
    url(r'^register/$', views.Register.as_view(), name='register'),

    url(r'^usernames/(?P<username>[a-zA-Z0-9_]{5,20})/count/$', views.UsernameCountView.as_view(), name='username_count'),
    url(r'^mobile/(?P<mobile>[a-zA-Z0-9_]{5,20})/count/$', views.MobileCountView.as_view(), name='mobile_count_view'),
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCode.as_view()),
    url(r'^sms_codes/(?P<mobile>[a-zA-Z0-9_]{5,20})/$', views.MobileCode.as_view(), name='mobile_code')
    # url = this.host + '/sms_codes/' + this.mobile + '/?image_code=' + this.image_code + '&image_code_id=' + this.image_code_id;
]

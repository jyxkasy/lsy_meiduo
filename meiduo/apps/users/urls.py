from django.conf.urls import url
from apps.users import views

urlpatterns = [
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^contents/$', views.IndexView.as_view(), name='contents'),
    url(r'^usernames/(?P<username>[a-zA-Z0-9_]{5,20})/count/$', views.UsernameCountView.as_view(), name='usernamecount'),
    url(r'^mobile/(?P<mobile>[a-zA-Z0-9_]{5,20})/count/$', views.MobileCountView.as_view(), name='mobilecountview'),
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCode.as_view()),

]

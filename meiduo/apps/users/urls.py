from django.conf.urls import url
from apps.users import views

urlpatterns = [
    url('^register/$', views.Register.as_view(), name='register'),
    url('^contents/$', views.IndexView.as_view(), name='contents'),

]

from django.conf.urls import url
from apps.users import views

urlpatterns = [
    url('^register/$', views.Register.as_view())
]

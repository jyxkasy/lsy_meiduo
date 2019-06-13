from django.conf.urls import url
from apps.contents import views

urlpatterns = [

    url(r'^contents/', views.IndexView.as_view(), name='contents')
]
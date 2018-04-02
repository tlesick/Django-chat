from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^homepage$', views.homepage, name='homepage'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]

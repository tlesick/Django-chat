
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^register$', views.register),
    url(r'^login$', views.login_process),
    url(r'^logout$', views.logout),
    url(r'^registration$', views.registration),
    
]

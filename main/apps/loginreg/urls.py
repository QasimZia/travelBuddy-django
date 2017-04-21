from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='loginIndex'),
    url(r'^process/create$', views.create, name='loginCreate'),
    url(r'^process/login$', views.login, name='loginLogin'),
    url(r'^success$', views.success, name='loginSuccess'),
    url(r'^logout$', views.signOut, name='signOut')
]
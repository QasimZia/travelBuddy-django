from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='travelsIndex'),
    url(r'^add$', views.add, name='addTravels'),
    url(r'^create$', views.create, name='createTravel'),
    url(r'^destination/(?P<id>\d+)$', views.destinationView, name='destinationView'),
    url(r'^joinTrip/(?P<id>\d+)$', views.joinTrip, name='tripJoin')
]
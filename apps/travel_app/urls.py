from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^reggy$', views.reggy), #proccess registration
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^trips/new/(?P<user_id>\d+)$', views.createpage),
    url(r'^create$', views.create),
    url(r'^delete/(?P<trip_id>\d+)$', views.delete),
    url(r'^show/(?P<trip_id>\d+)$', views.show),
    url(r'^update/(?P<trip_id>\d+)$', views.update),
    url(r'^trips/edit/(?P<trip_id>\d+)$', views.editpage),
]
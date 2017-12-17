
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^travels$', views.travels),
    url(r'^clear$',views.clear),
    url(r'^newtrip$',views.newtrip),
    url(r'^create_trip$',views.create_trip),
    url(r'^travels/destination/(?P<destination_id>[0-9]+)$',views.destination),
    url(r'^join/(?P<trip_id>[0-9]+)$',views.join_trip),
    url(r'^create$',views.create),
    url(r'^User/new$',views.new),
    url(r'^login$',views.login),
]


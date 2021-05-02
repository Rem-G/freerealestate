from django.urls import include, path, re_path
from . import views


urlpatterns = [
    #(?P<table>[A-z0-9_]+)
    re_path(r'findstation/(?P<station>[\w|\W]+)/', views.find_station_suggestions, name='station'),
    re_path(r'station/(?P<station>[\w|\W]+)/', views.get_station_infos, name='station'),
    re_path(r'createdb/', views.create_db, name='create_db'),
    re_path(r'test/', views.test),
    re_path(r'nextdeparture/(?P<station>[\w|\W]+)/', views.get_next_departure, name="get_next_departure"),
]
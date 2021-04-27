from django.urls import include, path, re_path
from . import views


urlpatterns = [
    #(?P<table>[A-z0-9_]+)
    re_path(r'station/(?P<station>[\w|\W]+)/', views.get_station_infos, name='station'),
    re_path(r'createdb/', views.create_db, name='create_db'),
]

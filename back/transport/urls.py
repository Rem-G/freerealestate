from django.urls import include, path, re_path
from . import views


urlpatterns = [
    re_path(r'findstation/(?P<station>[\w|\W]+)/', views.find_station_suggestions, name='station'),
    re_path(r'station/(?P<station>[\w|\W]+)/(?P<network>[\w|\W]+)', views.get_station_infos, name='station'),
    re_path(r'createdb/', views.create_db, name='create_db'),
    re_path(r'test/', views.test),
    re_path(r'getimage/(?P<line>[\w|\W]+)/(?P<network>[\w|\W]+)/', views.get_image_request),
    re_path(r'getgif/', views.get_gif_request),
    re_path(r'nextdepartures/(?P<station>[\w|\W]+)/(?P<network>[\w|\W]+)/', views.get_next_departures, name="get_next_departure"),
    re_path(r'topo/(?P<station>[\w|\W]+)/(?P<network>[\w|\W]+)/', views.get_topo_station, name="get_topo_station"),
    re_path(r'livebus/(?P<station>[\w|\W]+)/(?P<network>[\w|\W]+)/', views.get_live_bus, name="get_live_bus"),
    re_path(r'alert/(?P<network>[\w|\W]+)/(?P<station>[\w|\W]+)/(?P<type_a>[\w|\W]+)/', views.get_alertes_trafic, name="get_alertes_trafic"),
]
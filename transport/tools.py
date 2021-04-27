from .models import Station

def get_station_network(station):
	queryset = Station.objects.filter(station__contains = station)
	data = list(queryset.values())
	if len(data):
		return data
	else:
		return None

def add_station_db(station, network, station_type):
	Station.objects.get_or_create(station = station, network = network, station_type = station_type)


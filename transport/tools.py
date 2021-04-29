from .models import Station

def get_station_network(station):
	queryset = Station.objects.filter(station__contains = station)
	data = list(queryset.values())
	if len(data):
		return data
	else:
		return []

def add_station_db(station, network):
	Station.objects.update_or_create(station = station, network = network)

def drop_table():
	Station.objects.all().delete()



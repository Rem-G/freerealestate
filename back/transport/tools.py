from .models import Station
import requests

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

def request(url, headers={}):
	res = requests.get(url, headers=headers)

	if res.status_code == 200:
		return res.json()
	else:
		return []
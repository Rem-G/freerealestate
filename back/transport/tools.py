from .models import Station
import requests
import base64
from django.conf import settings
import shutil
from pathlib import Path

def get_image(line, network):
	ctx = dict()
	static_path = Path(settings.STATICFILES_DIRS[0])
	with open(f'{static_path}/img/{line}_{network}.png', "rb") as image_file:
		image_data = base64.b64encode(image_file.read()).decode('utf-8')

	ctx["image"] = image_data

	return ctx

def get_station_suggestions(station):
	queryset = Station.objects.filter(station__contains = station)
	data = list(queryset.values())
	if len(data):
		return data
	else:
		return []

def get_station(station, network):
	queryset = Station.objects.filter(station = station, network = network)
	data = list(queryset.values())
	if len(data):
		return data
	else:
		return []

def add_station_db(station, network, id_station = "", lat=2.349014, lon=48.864716):
	Station.objects.update_or_create(station = station, network = network, lat = lat, lon = lon, id_station = id_station)

def drop_table():
	Station.objects.all().delete()

def request(url, headers={}):
	res = requests.get(url, headers=headers)

	if res.status_code == 200:
		return res.json()
	else:
		return []
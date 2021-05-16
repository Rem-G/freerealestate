from .models import Station
import requests
import base64
from django.conf import settings
from pathlib import Path
import os.path

def get_image(line, network):
	static_path = Path(settings.STATICFILES_DIRS[0])
	if network == "Lyon":
		return {"image": f"https://www.tcl.fr/themes/custom/sytral_theme/img/lignes/{line}.svg", "type": "svg"}

	elif os.path.isfile(f'{static_path}/img/{line}_{network}.png'):
		with open(f'{static_path}/img/{line}_{network}.png', "rb") as image_file:
			image_data = base64.b64encode(image_file.read()).decode('utf-8')
		
		return {"image": image_data, "type": "png"}

	else:
		with open(f'{static_path}/img/notfound.png', "rb") as image_file:
			image_data = base64.b64encode(image_file.read()).decode('utf-8')
		return {"image": image_data, "type": "notfound"}


def get_gif():
	ctx = dict()
	static_path = Path(settings.STATICFILES_DIRS[0])

	with open(f'{static_path}/img/realtime.gif', "rb") as image_file:
		image_data = base64.b64encode(image_file.read()).decode('utf-8')
	
	ctx["gif"] = image_data

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

def add_station_db(station, network, lat=2.349014, lon=48.864716):
	Station.objects.update_or_create(station = station, network = network, lat = lat, lon = lon)

def drop_table():
	Station.objects.all().delete()

def request(url, headers={}):
	res = requests.get(url, headers=headers)

	if res.status_code == 200:
		return res.json()
	else:
		return []
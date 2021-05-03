from django.shortcuts import render
from django.http import JsonResponse

from .Star import Star
from .TCL import TCL
from .Ilevia import Ilevia
from .tools import *

star = Star()
tcl = TCL()
ilevia = Ilevia()

def find_station_suggestions(request, station):
	res = get_station_suggestions(station)
	return JsonResponse({"network": res})

def get_station_infos(request, station, network):
	res = get_station(station, network)
	return JsonResponse({"network": res})

def create_db(request):
	drop_table()
	tcl.create_stations_db()
	ilevia.create_stations_db()
	star.create_stations_db()
	ilevia.create_stations_db()
	return JsonResponse({"Done": True})

def test(request):
	ilevia.get_info_at_bus_or_streetcar_stop("fort de mons")
	ilevia.get_info_at_subway_stop("fort de mons")
	return JsonResponse({"Done": True})

def get_next_departure(request, station, network):
	res = []
	if network == 'Star':
		res = star.get_station_next_depart(station)
	elif network == 'TCL':
		res = tcl.get_station_next_depart(station)

	return JsonResponse({"next_departures": res})

def get_image_request(request, line, network):
	return JsonResponse({"ctx": get_image(line, network)})
	
def get_topo_station(request, station, network):
	res = []
	if network == 'Star':
		res = star.get_topo(station)

	return JsonResponse({"topo": res})

def get_live_bus(request, station, network):
	res = []
	if network == "Star":
		res = star.get_live_bus_station(station)

	return JsonResponse({"live": res})

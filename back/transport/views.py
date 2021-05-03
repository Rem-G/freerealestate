from django.shortcuts import render
from django.http import JsonResponse

from .Star import Star
from .TCL import TCL
from .Ilevia import Ilevia
from .tools import *

star = Star()
tcl = TCL()
ilevia = Ilevia()

def get_station_infos(request, station):
	res = get_station_network(station)
	return JsonResponse({"network": res})

def create_db(request):
	drop_table()
	# tcl.create_station_db()
	ilevia.create_stations_db()
	star.create_stations_db()
	return JsonResponse({"Done": True})

def test(request):
	ilevia.get_info_at_bus_or_streetcar_stop("fort de mons")
	ilevia.get_info_at_subway_stop("fort de mons")
	return JsonResponse({"Done": True})
	
def get_next_departure(request, station):
	res = star.get_station_next_depart(station)
	return JsonResponse({"next_departures": res})
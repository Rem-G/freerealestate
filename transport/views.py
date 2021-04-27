from django.shortcuts import render
from django.http import JsonResponse

from .Star import Star
from .tools import *

star = Star()

def get_station_infos(request, station):
	res = get_station_network(station)
	return JsonResponse({"network": res})

def create_db(request):
	star.create_stations_db()

	return JsonResponse({"Done": True})

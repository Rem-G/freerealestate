import requests
from django.conf import settings
import shutil
from pathlib import Path
from .tools import *

#https://data.explore.star.fr/explore/?sort=title

class Star:
	def __init__(self):
		self.network = "Star"

	def get_bus_stations(self):
		url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-topologie-pointsarret-td&q=&facet=nomstationparente&rows=10000"
		res = request(url)
		if len(res) > 0:
			return res.get("records")
		return []

	def get_metro_stations(self):
		url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-metro-topologie-pointsarret-td&q=&facet=nomstationparente&rows=10000"
		res = request(url)
		if len(res) > 0:
			return res.get("records")
		return []

	def add_to_db(self, data, stations):
		for station in data:
			name = station.get("fields").get("nom")
			if name not in stations:
				lat, lon = station.get("geometry").get("coordinates")
				add_station_db(name, self.network, lat, lon)
				stations.append(name)
		return stations


	def create_stations_db(self):
		stations = []
		stations = self.add_to_db(self.get_metro_stations(), stations)
		stations = self.add_to_db(self.get_bus_stations(), stations)
	
	def get_live_bus(self):
		url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-vehicules-position-tr&q=&facet=numerobus&facet=nomcourtligne&facet=sens&facet=destination&rows=10000"
		return request(url).get("records")

	def download_img_all(self):
		for transport in self.get_live_bus():
			self.download_img(transport)

		self.download_img({"fields": {"nomcourtligne": "a"}}, "metro")

	def download_img(self, transport, transport_type="bus"):
		if transport_type == "bus":
			url = f"https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-lignes-pictogrammes-dm&q=&facet=nomcourtligne&facet=date&facet=resolution&refine.nomcourtligne={transport.get('fields').get('nomcourtligne')}"
		else:
			url = f"https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-metro-lignes-pictogrammes-dm&q=&facet=nomcourtligne&facet=date&facet=resolution&refine.nomcourtligne={transport.get('fields').get('nomcourtligne')}"
		img_id = ""
		for img in request(url).get("records"):
			if img.get('fields').get('image').get("width") == 100:
				img_id = img.get('fields').get('image').get('id')

		if transport_type == "bus":
			line_img_url_dl = f"https://data.explore.star.fr/explore/dataset/tco-bus-lignes-pictogrammes-dm/files/{img_id}/download/"
		else:
			line_img_url_dl = f"https://data.explore.star.fr/explore/dataset/tco-metro-lignes-pictogrammes-dm/files/{img_id}/download/"

		r = requests.get(line_img_url_dl, stream = True)

		if r.status_code == 200:
			r.raw.decode_content = True
			path = Path(settings.STATICFILES_DIRS[0])
			with open(f"{path}/img/{transport.get('fields').get('nomcourtligne')}_{self.network}.png", "wb") as f:
				shutil.copyfileobj(r.raw, f)
			print('Image sucessfully Downloaded: ',img_id)
		else:
			print('Image Couldn\'t be retreived')
		
	def get_station_lines(self, station, transport_type="bus"):
 		url = f"https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-{transport_type}-topologie-dessertes-td&q=&facet=libellecourtparcours&facet=nomcourtligne&facet=nomarret&facet=estmonteeautorisee&facet=estdescenteautorisee&refine.nomarret={station}"
 		return set([line.get("fields").get("nomcourtligne") for line in request(url).get("records")])

	def get_topo(self, station):
		url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-topologie-parcours-td&q=&facet=idligne&facet=nomcourtligne&facet=senscommercial&facet=type&facet=nomarretdepart&facet=nomarretarrivee&facet=estaccessiblepmr&rows=10000"
		res = []
		station_lines = self.get_station_lines(station)

		for record in request(url).get("records"):
			if record.get("fields").get("nomcourtligne") in station_lines:
				res.append(record)

		metro_url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-metro-topologie-parcours-td&q=&facet=idligne&facet=nomcourtligne&facet=senscommercial&facet=type&facet=nomarretdepart&facet=nomarretarrivee&facet=estaccessiblepmr&rows=10000&refine.nomcourtligne=a"
		res += request(metro_url).get("records")

		return self.convert_coor_topo(res)

	def convert_coor_topo(self, records):
		for index, record in enumerate(records):
			for coor_index, coor in enumerate(record.get("fields").get("parcours").get("coordinates")):
				records[index]["fields"]["parcours"]["coordinates"][coor_index] = [coor[1], coor[0]]

		return records

	def convert_coor_live(self, records):
		for index, record in enumerate(records):
			coor = record["geometry"]["coordinates"]
			records[index]["geometry"]["coordinates"] = [coor[1], coor[0]]

		return records

	def get_live_bus_station(self, station):
		station_lines = self.get_station_lines(station)
		res = []

		for record in self.get_live_bus():
			if record.get("fields").get("nomcourtligne") in station_lines:
				res.append(record)		
		return self.convert_coor_live(res)
		 
	def get_station_next_depart(self, station):
		data = []
		#bus
		url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-topologie-dessertes-td&q=&sort=idparcours&facet=libellecourtparcours&facet=nomcourtligne&facet=nomarret&facet=estmonteeautorisee&facet=estdescenteautorisee&refine.nomarret={}".format(station)
		station_lines = request(url).get("records")

		#metro
		url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-metro-topologie-dessertes-td&q=&facet=libellecourtparcours&facet=nomcourtligne&facet=nomarret&facet=estmonteeautorisee&facet=estdescenteautorisee&refine.nomarret={}".format(station)
		station_lines += request(url).get("records")
		id_lines = set([line.get("fields").get("idligne") for line in station_lines])

		for id_line in id_lines:
			if id_line == "1001":#metro
				url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-metro-circulation-passages-tr&q=&sort=-depart&facet=nomcourtligne&facet=sens&facet=destination&facet=nomarret&facet=precision&facet=idligne&refine.idligne={}&rows=5&timezone=Europe/Paris".format(id_line)
			else:
				url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-circulation-passages-tr&q=&sort=-depart&facet=idligne&facet=nomcourtligne&facet=sens&facet=destination&facet=precision&facet=nomarret&refine.idligne={}&rows=5&timezone=Europe/Paris".format(id_line)
			
			line_infos = request(url).get("records")
			destinations = []
			lines = []

			for rec in line_infos:
				dest = rec.get("fields").get("destination")
				line = rec.get("fields").get("nomcourtligne")

				if not(dest in destinations and line in lines):
					data.append({"line": line, "destination": dest, "next_departure": rec.get("fields").get("depart")})
					destinations.append(dest)
					lines.append(line)
					
		return data





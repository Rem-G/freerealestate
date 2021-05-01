import requests
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





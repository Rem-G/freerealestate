import requests
from .tools import *

#https://data.explore.star.fr/explore/?sort=title

class Star:
    def __init__(self):
        self.network = "Star"

    def get_bus_stations(self):
        url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-topologie-dessertes-td&q=&facet=libellecourtparcours&facet=nomcourtligne&facet=nomarret&facet=estmonteeautorisee&facet=estdescenteautorisee&rows=10000"
        res = requests.get(url)

        if res.status_code == 200:
            res = res.json()
            return res.get("records")
        else:
            return []

    def get_metro_stations(self):
        url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-metro-topologie-dessertes-td&q=&facet=libellecourtparcours&facet=nomcourtligne&facet=nomarret&facet=estmonteeautorisee&facet=estdescenteautorisee&rows=10000"
        res = requests.get(url)

        if res.status_code == 200:
            res = res.json()
            return res.get("records")
        else:
            return []

    def create_stations_db(self):
        for metro_station in self.get_metro_stations():
            add_station_db(metro_station.get("fields").get("nomarret"), self.network)

        for bus_station in self.get_bus_stations():
            add_station_db(bus_station.get("fields").get("nomarret"), self.network)

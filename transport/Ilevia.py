# https://opendata.lillemetropole.fr/explore/?sort=modified&q=ilevia

import requests
import json

class IleviaNetwork:

    def __init__(self):

        url_bus_stop = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=arrets-bus&rows=10000"
        url_streetcar_stop = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=tramway-arrets&rows=10000"
        url_subway_stop = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=stations-metro&rows=10000"

        self.response_bus_stop = requests.get(url_bus_stop).json()
        self.response_streetcar_stop = requests.get(url_streetcar_stop).json()
        self.response_subway_stop = requests.get(url_subway_stop).json()

    def create_stations_db():
        pass

    def get_bus_stops(self):
        return [record["fields"]["name"].upper() for record in self.response_bus_stop["records"]]

    def get_streetcar_stops(self):
        return [record["fields"]["nom_statio"].upper() for record in self.response_streetcar_stop["records"]]

    def get_subway_stops(self):
        return [record["fields"]["nom_statio"].upper() for record in self.response_streetcar_stop["records"]]

    def get_info_at_stop(self, stop):
        stop = stop.upper()

        bus_stops = self.get_bus_stops()
        streetcar_stops = self.get_streetcar_stops()
        # subway_stops = self.get_subway_stops()        A AJOUTER

        info = list()

        url_passage = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=ilevia-prochainspassages&q=&rows=10000&sort=cletri&facet=nomstation&refine.nomstation={}"

        if stop in bus_stops:
            response_passage = requests.get(url_passage.format(stop)).json()

            for record in response_passage["records"]:
                info.append({"direction" : record["fields"]["sensligne"], "horraire" : record["fields"]["heureestimeedepart"], "type" : "Bus"})

        if stop in streetcar_stops:
            response_passage = requests.get(url_passage.format(stop)).json()

            for record in response_passage["records"]:
                info.append({"direction" : record["fields"]["sensligne"], "horraire" : record["fields"]["heureestimeedepart"], "type" : "Bus"})

        return info

test = IleviaNetwork()
print(test.get_info_at_stop("2 nations"))
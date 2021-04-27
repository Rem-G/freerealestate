# https://public.opendatasoft.com/api/records/1.0/search/?dataset=lignes-de-metro-et-funiculaire-du-reseau-tcl-grand-lyon&q=&facet=code_titan&facet=sens&facet=libelle&facet=ut&facet=couleur&facet=last_upd_1&rows=10000
# https://public.opendatasoft.com/api/records/1.0/search/?dataset=lignes-de-bus-du-reseau-tcl-grand-lyon&facet=code_titan&facet=sens&facet=libelle&facet=ut&facet=couleur&facet=last_upd_1&rows=10000
# https://public.opendatasoft.com/api/records/1.0/search/?dataset=lignes-de-tramway-du-reseau-tcl-grand-lyon&facet=code_titan&facet=sens&facet=libelle&facet=ut&facet=couleur&facet=last_upd_1&rows=10000

# https://download.data.grandlyon.com/ws/rdata/tcl_sytral.tclarret/all.json?maxfeatures=-1&start=1

import requests
from .tools import *

class Tcl:
    def __init__(self) -> None:
        self.network = "Tcl"
        self.data = requests.get("https://download.data.grandlyon.com/ws/rdata/tcl_sytral.tclarret/all.json?maxfeatures=-1&start=1")
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def get_bus_stations(self) -> list:
        url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=lignes-de-bus-du-reseau-tcl-grand-lyon&facet=code_titan&facet=sens&facet=libelle&facet=ut&facet=couleur&facet=last_upd_1&rows=10000"
        bus = requests.get(url, headers = self.headers)
        ligne = []
        for i in bus.json()["records"]:
            titan = i["fields"]["code_titan"].upper()
            titan = titan[0:-2] + ":" + titan[-2:-1]
            ligne.append(titan)

        bus_id = []
        for stop in self.data.json()["values"]:
            dessert = stop["desserte"].split(",")
            if len(list(set(dessert).intersection(ligne))) > 0:
                bus_id.append(stop['nom'])

        return bus_id

    def create_station_db(self):
        for bus_station in self.get_bus_stations():
            add_station_db(bus_station, self.network, "bus")
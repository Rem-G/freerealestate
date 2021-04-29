# https://opendata.lillemetropole.fr/explore/?sort=modified&q=ilevia

import requests
import json
import pandas as pd
from .tools import *

class Ilevia:

    def __init__(self):
        self.network = "Ilevia"

    def get_bus_stops(self):
        url_bus_stop = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=arrets-bus&rows=10000"
        response_bus_stop = requests.get(url_bus_stop).json()
        return [record["fields"]["name"].upper() for record in response_bus_stop["records"]]

    def get_streetcar_stops(self):
        url_streetcar_stop = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=tramway-arrets&rows=10000"
        response_streetcar_stop = requests.get(url_streetcar_stop).json()
        return [record["fields"]["nom_statio"].upper() for record in response_streetcar_stop["records"]]


    def get_subway_stops(self):
        url_subway_stop = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=stations-metro&rows=10000"
        response_subway_stop = requests.get(url_subway_stop).json()
        return [record["fields"]["nom_statio"].upper() for record in response_subway_stop["records"]]


    def create_stations_db(self):
        for metro_station in self.get_subway_stops():
            add_station_db(metro_station, self.network)

        for bus_station in self.get_bus_stops():
            add_station_db(bus_station, self.network)

        for streetcar_station in self.get_streetcar_stops():
            add_station_db(streetcar_station, self.network)


    def get_info_at_bus_or_streetcar_stop(self, stop):
        stop = stop.upper()
        info = list()

        url_passage = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=ilevia-prochainspassages&q=&rows=10000&sort=cletri&facet=nomstation&refine.nomstation={}"
        response_passage = requests.get(url_passage.format(stop)).json()

        for record in response_passage["records"]:
            info.append({"ligne" : record["fields"]["codeligne"],
                        "direction" : record["fields"]["sensligne"],
                        "horraire" : record["fields"]["heureestimeedepart"]})

        return info

    def get_subway_data(self):
        subway_stops_df = pd.read_csv("static/gtfs_Ilevia/stops.txt")
        subway_stops_df = subway_stops_df.loc[:, ['stop_name','stop_id']]

        subway_stop_times_df = pd.read_csv("static/gtfs_Ilevia/stop_times.txt")
        subway_stop_times_df = subway_stop_times_df.loc[:, ['stop_id','trip_id']]

        subway_routes_df = pd.read_csv('static/gtfs_Ilevia/routes.txt')
        subway_routes_df = subway_routes_df[subway_routes_df["route_id"].str.contains("(ME1|ME2)[^R]")] # REGEX A REVOIR
        print("\n\nTEST\n", subway_routes_df.head(5), "\n")
        subway_routes_df = subway_routes_df.loc[:,['route_id','route_short_name']]

        subway_trips_df = pd.read_csv('static/gtfs_Ilevia/trips.txt')
        subway_trips_df = subway_trips_df.loc[:,['route_id', 'trip_id']]

        subway_stop_times_df = subway_stop_times_df.loc[range(100), :]

        id_ = []
        nom = []
        nom_arretb =[]
        for i in range(len(subway_stop_times_df)):
            id_route = str(list(subway_trips_df[subway_trips_df['trip_id'] == subway_stop_times_df.loc[i,'trip_id']]['route_id'])[0])
            print("\n\nTEST\n", subway_routes_df[subway_routes_df['route_id'] == id_route]['route_short_name'], "\n")
            nom_route =  str(list(subway_routes_df[subway_routes_df['route_id'] == id_route]['route_short_name'])[0])
            nom_arret = str(list(subway_stops_df[subway_stops_df['stop_id'] == str(subway_stop_times_df.loc[i,'stop_id'])]['stop_name'])[0])

            id_.append(id_route)
            nom.append(nom_route)
            nom_arretb.append(nom_arret)


        subway_stop_times_df['id_route'] =  id_
        subway_stop_times_df['nom_route'] = nom
        subway_stop_times_df['nom_arret'] = nom_arretb


        del subway_stop_times_df['trip_id']
        subway_stop_times_df = subway_stop_times_df.drop_duplicates()

        print(subway_stop_times_df.head(5))

        return 0

    def get_info_at_subway_stop(self, stop):
        pass
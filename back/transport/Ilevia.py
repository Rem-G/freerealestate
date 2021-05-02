# https://opendata.lillemetropole.fr/explore/?sort=modified&q=ilevia

from django.conf import settings
import requests
import json
import pandas as pd
import numpy as np
from .tools import *

class Ilevia:

    def __init__(self):
        self.network = "Ilevia"
        self.static_path = settings.STATICFILES_DIRS[0]
        print(self.static_path+"/gtfs_Ilevia/stops.txt")

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

        print(info)

        return info

    # https://mrcagney.github.io/gtfstk_docs/
    # https://towardsdatascience.com/python-for-gtfs-segment-frequencies-in-a-map-4dc3bc1e26ff

    def get_info_at_subway_stop(self, stop):
        subway_stops_df = pd.read_csv(self.static_path+"/gtfs_Ilevia/stops.txt")
        subway_stops_df = subway_stops_df.loc[:, ['stop_name','stop_id']]

        subway_calendar_date_df = pd.read_csv(self.static_path+"/gtfs_Ilevia/calendar_dates.txt")
        subway_calendar_date_df = subway_calendar_date_df[subway_calendar_date_df["service_id"].str.contains("[^R](ME1|ME2)")]
        subway_calendar_date_df = subway_calendar_date_df.loc[:, ['service_id']]

        print(subway_calendar_date_df)

        subway_stop_times_df = pd.read_csv(self.static_path+"/gtfs_Ilevia/stop_times.txt")
        subway_stop_times_df = subway_stop_times_df.loc[:, ['stop_id','trip_id', 'departure_time']]

        subway_routes_df = pd.read_csv(self.static_path+'/gtfs_Ilevia/routes.txt')
        subway_routes_df = subway_routes_df[subway_routes_df["route_id"].str.contains("^(ME1|ME2)")]
        subway_routes_df = subway_routes_df.loc[:,['route_id','route_short_name']]

        subway_trips_df = pd.read_csv(self.static_path+'/gtfs_Ilevia/trips.txt')
        subway_trips_df = subway_trips_df[subway_trips_df["route_id"].str.contains("^(ME1|ME2)")]
        subway_trips_df = subway_trips_df.loc[:,['route_id', 'trip_id', 'service_id']]

        subway_stops_df["stop_name"] = subway_stops_df["stop_name"].apply(lambda x: x.upper())
        subway_stops_df = subway_stops_df[subway_stops_df["stop_name"] == stop.upper()]

        trip_ids = subway_trips_df['trip_id'].unique()

        stop_ids = subway_stops_df["stop_id"].unique()
        print("\n\nSTOPS IDS :\n", stop_ids)

        # route_id = str(list(subway_trips_df[subway_trips_df['route_id'] == "ME2"]['trip_id'])).split("'")[1]
        subway_stop_times_df = subway_stop_times_df[subway_stop_times_df["stop_id"] == stop_ids[1]]

        for index, row in subway_stop_times_df.iterrows():
            if row['departure_time'].split(":")[0] == "24":
                subway_stop_times_df.loc[index, 'departure_time'] = ":".join(["00"] + row['departure_time'].split(":")[1:])

            elif row['departure_time'].split(":")[0] == "25":
                subway_stop_times_df.loc[index, 'departure_time'] = ":".join(["00"] + row['departure_time'].split(":")[1:])

        subway_stop_times_df['departure_time'] = pd.to_datetime(subway_stop_times_df.departure_time, format='%H:%M:%S').dt.time
        # subway_stop_times_df.sort_values('departure_time', ascending=True)

        print(trip_ids[0])
        subway_stop_times_df = subway_stop_times_df[subway_stop_times_df['trip_id'] == 4139592]

        subway_stop_times_df.set_index('departure_time', verify_integrity=False)
        subway_stop_times_df = subway_stop_times_df.sort_index()

        print(subway_stop_times_df)

        #subway_stop_times_df = subway_stop_times_df[subway_stop_times_df["trip_id"].isin(trip_ids)]

        # id_ = []
        # names = []
        # stops_name =[]
        # for i in range(len(subway_stop_times_df)):
        #     print((i/len(subway_stop_times_df))*100,"%")
        #     route_id = str(list(subway_trips_df[subway_trips_df['trip_id'] == subway_stop_times_df.iloc[i]['trip_id']]['route_id'])).split("'")[1]
        #     route_name =  str(list(subway_routes_df[subway_routes_df['route_id'] == route_id]['route_short_name']))
        #     stop_name = str(list(subway_stops_df[subway_stops_df['stop_id'] == str(subway_stop_times_df.iloc[i]['stop_id'])]['stop_name']))

        #     id_.append(route_id)
        #     names.append(route_name)
        #     stops_name.append(stop_name)

        # subway_stop_times_df['route_id'] =  id_
        # subway_stop_times_df['route_name'] = names
        # subway_stop_times_df['stop_name'] = stops_name

        # del subway_stop_times_df['trip_id']
        # subway_stop_times_df = subway_stop_times_df.drop_duplicates()

        # print(subway_stop_times_df.head(100))

        return 0
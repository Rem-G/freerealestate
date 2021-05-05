from datetime import datetime, time
from .tools import *
from django.conf import settings
import datetime
import pandas as pd
import os
class TCL:
    def __init__(self) -> None:
        self.network = "Lyon"
        self.static_path = settings.STATICFILES_DIRS[0]
        self.df = pd.read_parquet(f'{self.static_path}/gtfs_tcl/arrets.parquet.gzip')
        self.calendar =  pd.read_parquet(f'{self.static_path}/gtfs_tcl/calendar.parquet.gzip')
        self.trips =  pd.read_parquet(f'{self.static_path}/gtfs_tcl/trips.parquet.gzip')

    def create_stations_db(self):
        for i in self.df.index:
            add_station_db(station = self.df["stop_name"][i], network=self.network, lat=self.df["lat"][i], lon=self.df["lon"][i], id_station=self.df["stop_id"][i])

    def rechercheService(self,stop_id, jour):
        heure = []
        id_route = list(self.df[self.df['stop_id'] == stop_id]['id_route'])[0]
        trip = list(set(self.trips[self.trips['route_id'] == id_route]['service_id']))
        for t in trip:
            typeT = self.calendar[self.calendar['service_id'] == t]
            if(list(typeT[jour])[0] == 1):
                return t

    def rechercheHeure(self,stop_id, jour):
        path = "./dataV2/"
        service = self.rechercheService(stop_id, jour)
        type_transport = list(self.df[self.df['stop_id'] == stop_id]['type'])[0]
        ensembleTrips = list(set(self.trips[self.trips['service_id'] == service]['trip_id']))
        data = pd.read_parquet(f'{self.static_path}/gtfs_tcl/{type_transport}/{stop_id}.parquet.gzip')
        return sorted(data[data['trip_id'].isin(ensembleTrips)]['departure_time'])


    def get_station_next_depart(self, station):
        data = []
        actuel = datetime.datetime.now().strftime('%H:%M:%S')
        semaine = {0: 'monday',1: 'tuesday',2: 'wednesday',3: 'thursday',4: 'friday',5:'saturday',6: 'sunday'}
        jour = semaine[datetime.datetime.today().weekday()]
        try:
            station = int(station)
        except:
            pass

        if type(station) == str:
            stations = self.df[self.df["stop_name"] == station]
            for sta in stations.index:
                heures = self.rechercheHeure(stations['stop_id'][sta], jour)
                donnee = []
                for i in heures:
                    if len(donnee) > 5:
                        break
                    if(i > actuel):
                        donnee.append(i)
                data.append({"line": stations['short_name'][sta], "destination": stations['destination'][sta], "next_departure": donnee})
            return data

        else:
            stations = self.df[self.df["stop_id"] == station]
            heures = self.rechercheHeure(int(stations['stop_id']), jour)
            donnee = []
            for i in heures:
                if len(donnee) > 5:
                    break
                if(i > actuel):
                    donnee.append(i)
            data.append({"line": list(stations['short_name'])[0], "destination": list(stations['destination'])[0],"next_departure": donnee})
            return data

    def get_alertes_trafic(self, id_station, type_a):

        url = "https://download.data.grandlyon.com/ws/rdata/tcl_sytral.tclalertetrafic_2/all.json?maxfeatures=-1&start=1"
        payload={}
        headers = {'Authorization': 'Basic bG9pYy52aWV1QGV0dS51bml2LXNtYi5mcjpsb2xvbGlBOTw='}
        response = requests.request("GET", url, headers=headers, data=payload)
        trafic_alertes = response.json()['values']
        ar = []
        # =======================================
        if type_a == "0":
            id_station = int(id_station)
            short_n = self.df[self.df["stop_id"] == id_station]["short_name"].values[0].upper()
            print(short_n)
            for alerte in trafic_alertes:
                if alerte['ligne_cli'].upper() == short_n:
                    ar.append(alerte)
            return ar

        # =======================================
        elif type_a == "1":
            stations = self.df[self.df["stop_name"] == id_station]
            for station in stations.index:
                # print(station)
                ligne = stations["short_name"][station]
                for alerte in trafic_alertes:
                    if alerte['ligne_cli'].upper() == ligne.upper():
                        ar.append(alerte)
            return ar

        elif type_a == "2":
            for alerte in trafic_alertes:
                if alerte['type'] == 'Perturbation majeure':
                    ar.append(alerte)
            return ar
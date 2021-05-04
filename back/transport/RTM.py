from datetime import datetime, time
from .tools import *
from django.conf import settings
import datetime
import pandas as pd
import os
class RTM:
    def __init__(self) -> None:
        self.network = "RTM"
        self.static_path = settings.STATICFILES_DIRS[0]
        self.df = pd.read_parquet(f'{self.static_path}/gtfs_rtm/arrets.parquet.gzip')
        self.calendar =  pd.read_parquet(f'{self.static_path}/gtfs_rtm/calendar.parquet.gzip')
        self.trips =  pd.read_parquet(f'{self.static_path}/gtfs_rtm/trips.parquet.gzip')

    def create_stations_db(self):
        for i in self.df.index:
            add_station_db(self.df["stop_name"][i], self.network, self.df["lat"][i], self.df["lon"][i])

    def rechercheService(self,stop_id, jour):
        heure = []
        id_route = list(self.df[self.df['stop_id'] == stop_id]['id_route'])[0]
        trip = list(set(self.trips[self.trips['route_id'] == id_route]['service_id']))
        for t in trip:
            typeT = self.calendar[self.calendar['service_id'] == t]
            if(list(typeT[jour])[0] == 1):
                return t

    def rechercheHeure(self,stop_id, jour):
        service = self.rechercheService(stop_id, jour)
        type_transport = list(self.df[self.df['stop_id'] == stop_id]['type'])[0]
        ensembleTrips = list(set(self.trips[self.trips['service_id'] == service]['trip_id']))
        data = pd.read_parquet(f'{self.static_path}/gtfs_rtm/{type_transport}/{stop_id}.parquet.gzip')
        return sorted(data[data['trip_id'].isin(ensembleTrips)]['departure_time'])


    def get_station_next_depart(self, station):
        data = []
        actuel = datetime.datetime.now().strftime('%H:%M:%S')
        semaine = {0: 'monday',1: 'tuesday',2: 'wednesday',3: 'thursday',4: 'friday',5:'saturday',6: 'sunday'}
        jour = semaine[ datetime.datetime.today().weekday()]
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


    def tempsReel(self, stop_id):
        url = "https://download.data.grandlyon.com/ws/rdata/tcl_sytral.tclpassagearret/all.json?maxfeatures=10000&start=1"
        payload={}
        headers = {'Authorization': 'Basic bG9pYy52aWV1QGV0dS51bml2LXNtYi5mcjpsb2xvbGlBOTw='}
        boucle = True
        while boucle:
            response = requests.request("GET", url, headers=headers, data=payload)
            newDf= pd.DataFrame.from_dict(response.json()['values'])
            if len(newDf[newDf["id"] == stop_id]) == 0:
                print(response.json().keys())
                if('next' in response.json().keys()):
                    url = response.json()['next']
                else:
                    boucle = False
            else:
                return list(newDf[newDf["id"] == stop_id]["heurepassage"])
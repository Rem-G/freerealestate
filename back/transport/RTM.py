from datetime import datetime, time
from .tools import *
from django.conf import settings
import datetime
import pandas as pd
import os
class RTM:
    """
    This class process all request for Marseille/RTM network.
    All answers are standardized.
    """
    def __init__(self) -> None:
        self.network = "Marseille"
        self.static_path = settings.STATICFILES_DIRS[0]
        self.df = pd.read_parquet(f'{self.static_path}/gtfs_rtm/arrets.parquet.gzip')
        self.calendar =  pd.read_parquet(f'{self.static_path}/gtfs_rtm/calendar.parquet.gzip')
        self.trips =  pd.read_parquet(f'{self.static_path}/gtfs_rtm/trips.parquet.gzip')


    def create_stations_db(self):
        """
			Add stations to DB
			To prevent duplicates, the method return the list of inserted stations
		"""
        newDf = self.df.loc[:, 'stop_name'].drop_duplicates()
        for i in newDf.index:
            lat = self.df[self.df["stop_name"] == newDf[i]]['lat'].values[0]
            lon = self.df[self.df["stop_name"] == newDf[i]]['lon'].values[0]
            add_station_db(station = newDf[i], network= self.network, lat=lat, lon=lon)

    def rechercheService(self,stop_id, jour):
        """
        Find correct service for a stop_id and day given
        """
        heure = []
        id_route = list(self.df[self.df['stop_id'] == stop_id]['id_route'])[0]
        trip = list(set(self.trips[self.trips['route_id'] == id_route]['service_id']))
        for t in trip:
            typeT = self.calendar[self.calendar['service_id'] == t]
            if(list(typeT[jour])[0] == 1):
                return t

    def rechercheHeure(self,stop_id, jour):
        """
        Return all hours for a stop and a day (monday ...)
        """
        path = "./dataV2/"
        service = self.rechercheService(stop_id, jour)
        type_transport = list(self.df[self.df['stop_id'] == stop_id]['type'])[0]
        ensembleTrips = list(set(self.trips[self.trips['service_id'] == service]['trip_id']))
        data = pd.read_parquet(f'{self.static_path}/gtfs_rtm/{type_transport}/{stop_id}.parquet.gzip')
        return sorted(data[data['trip_id'].isin(ensembleTrips)]['departure_time'])

    def get_station_next_depart(self, station):
        """
			Get 3 next departures at a given station
		"""
        data = []
        actuel = datetime.datetime.now().strftime('%H:%M:%S')
        semaine = {0: 'monday',1: 'tuesday',2: 'wednesday',3: 'thursday',4: 'friday',5:'saturday',6: 'sunday'}
        jour = semaine[datetime.datetime.today().weekday()]


        stations = self.df[self.df["stop_name"] == station]
        for sta in stations.index:
            if stations['stop_name'][sta] != stations['destination'][sta]: #Ne pas afficher les heures si nous sommes au terminus
                heures = self.rechercheHeure(stations['stop_id'][sta], jour)
                donnee = []
                for i in heures:
                    if len(donnee) > 3:
                        break
                    if(i > actuel):
                        newH = i.split(':')
                        newH = f'{newH[0]}:{newH[1]}'
                        donnee.append(newH)

                data.append({"line": stations['short_name'][sta], "destination": stations['destination'][sta], "next_departures": donnee})
        return data

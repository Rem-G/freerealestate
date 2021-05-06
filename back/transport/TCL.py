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
        self.topo = {}

    def create_stations_db(self):
        newDf = self.df.loc[:, 'stop_name'].drop_duplicates()
        for i in newDf.index:
            lat = self.df[self.df["stop_name"] == newDf[i]]['lat'].values[0]
            lon = self.df[self.df["stop_name"] == newDf[i]]['lon'].values[0]
            add_station_db(station = newDf[i], network= self.network, lat=lat, lon=lon)

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
                    if len(donnee) > 3:
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

    # allert sur le résaux
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

        # =======================================
        elif type_a == "2":
            ligne = []
            ar = {}
            ar['TRAM'] = []
            ar['BUS'] = []
            ar['METRO'] = []
            for alerte in trafic_alertes:
                if (alerte['type'] == 'Perturbation majeure' or alerte['mode'] == 'Métro')and alerte['ligne_cli'] not in ligne:
                    type_t = list(self.df[self.df['short_name'] == alerte['ligne_cli']]['type'])
                    if (len(type_t) > 0):
                        type_t = type_t[0]
                        if type_t == 'FUNICULAIRE':
                            type_t = "METRO"
                        if type_t == 'BUS' or type_t == 'TRAM' or type_t == "METRO":
                            ar[type_t].append(alerte)
                            ligne.append(alerte['ligne_cli'])
            return ar







    def get_topo_req(self):
        self.topo['METRO'] = requests.get("https://public.opendatasoft.com/api/records/1.0/search/?dataset=lignes-de-metro-et-funiculaire-du-reseau-tcl-grand-lyon&q=&rows=10000&facet=geo_point_2d&facet=code_titan&facet=sens&facet=libelle&facet=ut&facet=couleur&facet=last_upd_1").json()['records']
        self.topo['BUS'] = requests.get("https://public.opendatasoft.com/api/records/1.0/search/?dataset=lignes-de-bus-du-reseau-tcl-grand-lyon&q=&rows=10000&facet=sens&facet=infos&facet=couleur&facet=last_upd_1").json()['records']
        self.topo['TRAM'] = requests.get("https://public.opendatasoft.com/api/records/1.0/search/?dataset=lignes-de-tramway-du-reseau-tcl-grand-lyon&q=&rows=10000&facet=geo_point_2d&facet=code_titan&facet=ligne&facet=sens&facet=libelle&facet=ut&facet=couleur&facet=last_upd_1").json()['records']

    def get_topo(self, station):
        res = []
        def recherche(dict_c, nom, res):
            for i in dict_c:
                if i['fields']['ligne'] == nom:
                    new = {'fields': {}}
                    conver = i['fields']['couleur'].split(' ')
                    new['fields']['couleurtrace']  = '#%02x%02x%02x' % (int(conver[0]), int(conver[1]), int(conver[2]))
                    new['fields']['parcours'] = {}
                    coo = []
                    for j in i['fields']['geo_shape']['coordinates']:
                        coo.append([j[1],j[0]])
                        # for u in j:
                        #     coo2.append([u[1], u[0]])
                        # coo.append(coo2)
                    new['fields']['parcours']['coordinates'] = coo
                    new['fields']['nomcourtLigne'] = i['fields']['ligne']
                    res.append(new)
            return res

        if self.topo == {}: 
            self.get_topo_req()

        df_stations = self.df[self.df['stop_name'] == station]
        for station in df_stations.index:
            type_t = df_stations['type'][station]
            if type_t == "FUNICULAIRE":
                type_t = "METRO"
            nam_s = df_stations['short_name'][station]
            recherche(self.topo[type_t], nam_s,res)

        return res
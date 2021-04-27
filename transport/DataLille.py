# https://opendata.lillemetropole.fr/explore/?sort=modified&q=ilevia

import requests
import json
import pandas as pd

url_passage = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=ilevia-prochainspassages&q=&rows=10&sort=cletri&facet=nomstation&facet=codeligne&facet=sensligne&refine.nomstation=HOTEL+DE+VILLE&refine.codeligne=10&refine.sensligne=LOMME+HEGEL"
url_bus_stop = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=arrets-bus&rows=1489"
url_streetcar_stop = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=tramway-arrets&rows=66"

response_passage = requests.get(url_passage).json()
response_bus_stop = requests.get(url_bus_stop).json()
response_streetcar_stop = requests.get(url_streetcar_stop).json()

print(len(response_streetcar_stop["records"]))

bus_stops = list()
for i in range(1489):
    name = str(response_bus_stop["records"][i]["fields"]["label"])
    bus_stops.append(name)

streetcar_stops = list()
for i in range(66):
    name = str(response_streetcar_stop["records"][i]["fields"]["libelle"])
    streetcar_stops.append(name)

# print(bus_stops)
# print(streetcar_stops)

# bus_stop_df = pd.DataFrame(list(response_bus_stop.values()))

# print()
# print(bus_stop_df.head(5))
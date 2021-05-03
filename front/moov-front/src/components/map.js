
import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap, Polyline } from 'react-leaflet'
import L from 'leaflet';
import axios from "axios";
import 'leaflet/dist/leaflet.css';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow
});

L.Marker.prototype.options.icon = DefaultIcon;

function ChangeView({center, zoom}) {
    if (center == [48.864716, 2.349014]){ zoom = 7 }
    const map = useMap();
    map.setView(center, zoom);
    return null;
  } 

export default function Map({station}){
    const [liveBus, updateLiveBus] = useState([]);

    const fetchStarLiveBus = () => {
      axios
        .get("https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-vehicules-geoposition-suivi-new-billetique-tr&q=&rows=10000")
        .then(response => {
          updateLiveBus(response.data.records);
        })
        .catch(err => {console.log(err);});
    }

    const fetchStarLines = () => {
      axios.get("")
    }

    useEffect(() => {
      if (station.network == "Star"){
        // setInterval(() => {fetchLiveBus();}, 60000);
        fetchStarLiveBus();
      }
    // eslint-disable-next-line
    }, [station]);

    const position = [48.864716, 2.349014];
    return(
      <MapContainer center={position} zoom={7} scrollWheelZoom={false} style={{ height: "100%", width: "auto" }}>
          {station &&
            <ChangeView center={[station.lon, station.lat]} zoom={19}/>
          }
        <TileLayer
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png"
        />
        {liveBus.length > 0 && 
          liveBus.map((bus, index) => {
            // const imgUrl = "../static/img/"+bus.fields.nomcourtligne+".png";
            const position = [bus.geometry.coordinates[1], bus.geometry.coordinates[0]];
            const icon = new L.icon({
              iconUrl: "https://i.ya-webdesign.com/images/sample-png-image-download-3.png",          
              iconSize:     [30, 30], // size of the icon
              iconAnchor:   {position}, // point of the icon which will correspond to marker's location
              // popupAnchor:  {position} // point from which the popup should open relative to the iconAnchor
            });
            return (<Marker id={index} position={position} icon={icon} >
              <Popup>{bus.fields.nomcourtligne} destination {bus.fields.destination}</Popup>
            </Marker>)
          })
        }
      </MapContainer>
    )

}


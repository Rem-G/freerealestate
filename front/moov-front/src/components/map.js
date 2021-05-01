
import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
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
    const [imgUrl, updateImgUrl] = useState("");

    const fetchLiveBus = () => {
      axios
        .get("https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-vehicules-geoposition-suivi-new-billetique-tr&q=&rows=10000")
        .then(response => {
          updateLiveBus(response.data.records);
        })
        .catch(err => {console.log(err);});
    }

    const getIconUrl = (bus) => {
      let tempImgUrl = "";
      axios
        .get("https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-lignes-pictogrammes-dm&q=&facet=nomcourtligne&facet=date&facet=resolution&refine.nomcourtligne="+bus.fields.nomcourtligne)
        .then(response => {
          tempImgUrl = "https://data.explore.star.fr/explore/dataset/tco-bus-lignes-pictogrammes-dm/files/"+response.data.records[0].fields.image.id+"/22/";
          tempImgUrl = "https://findicons.com/files/icons/2219/dot_pictograms/256/bus.png";
          // console.log(imgUrl);
          updateImgUrl(tempImgUrl);
        })
        .catch(err => {console.log(err);});

      return imgUrl;
    }

    useEffect(() => {
      if (station.network == "Star"){
        fetchLiveBus();
      }
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
            getIconUrl(bus);
            console.log(imgUrl);
            return (<Marker id={index} position={[bus.geometry.coordinates[1], bus.geometry.coordinates[0]]} icon={
              L.icon({
              iconUrl: {imgUrl},
              // shadowUrl: 'leaf-shadow.png',
          
              iconSize:     [38, 95], // size of the icon
              shadowSize:   [50, 64], // size of the shadow
              iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
              shadowAnchor: [4, 62],  // the same for the shadow
              popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
          })} ></Marker>)
        })
        }
        <Marker position={position}>
          {/* <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
          </Popup> */}
        </Marker>
      </MapContainer>
    )

}


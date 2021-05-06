
import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap, Polyline, Tooltip } from 'react-leaflet'
import L from 'leaflet';
import axios from "axios";
import BusPopup from "./busPopup";
import MapLegend from './mapLegend';

import 'leaflet/dist/leaflet.css';
import "../style/map.css";
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow
});

L.Marker.prototype.options.icon = DefaultIcon;

function ChangeView({center, zoom}) {
    if (center === [48.864716, 2.349014]){ zoom = 7 }
    const map = useMap();
    map.setView(center, zoom);
    return null;
  } 

export default function Map({station}){
    const [liveBus, updateLiveBus] = useState([]);
    const [lines, updateLines] = useState([]);

    const fetchStarLiveBus = () => {
      axios
        .get("http://localhost:8000/api/transport/livebus/"+station.station+"/"+station.network)
        .then(response => {
          updateLiveBus(response.data.live);
        })
        .catch(err => {console.log(err);});
      }

    const fetchStarLines = () => {
      axios.get("http://localhost:8000/api/transport/topo/"+station.station+"/"+station.network)
      .then(response => {
        updateLines(response.data.topo);
        })
      .catch(err => {console.log(err);});
    }

    useEffect(() => {
      if (station.network === "Rennes" || station.network === "Lyon"){
        // setInterval(() => {fetchLiveBus();}, 60000);
        fetchStarLines();
        fetchStarLiveBus();
      }
    // eslint-disable-next-line
    }, [station]);

    const getCurrentLatLon = (e) => {
      console.log("ok");
      console.log(e);
    }

    const position = [48.864716, 2.349014];
    return(
      <div>
        <div className="map">
          <MapContainer center={position} zoom={7} scrollWheelZoom={false} style={{ height: "100%", width: "auto" }}>
              {station &&
                <ChangeView center={[station.lat, station.lon]} zoom={19}/>
              }
            <TileLayer
              attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
              url='https://{s}.tile.jawg.io/jawg-light/{z}/{x}/{y}{r}.png?access-token=lSEGnNTOJVtlgrq2PsWaiy9iNmnRuwn2qtVunwPUuhBEPIiQo2pdfaHRIjukcPft'
            />
            {liveBus.length > 0 && 
              liveBus.map((bus, index) => {
                // const imgUrl = "../static/img/"+bus.fields.nomcourtligne+".png";
                const position = bus.geometry.coordinates;
                const icon = new L.icon({
                  iconUrl: "https://i.ya-webdesign.com/images/sample-png-image-download-3.png",          
                  iconSize:     [30, 30], // size of the icon
                  iconAnchor:   {position}, // point of the icon which will correspond to marker's location
                  // popupAnchor:  {position} // point from which the popup should open relative to the iconAnchor
                });
                return (<Marker id={index} position={position} icon={icon} >
                  <BusPopup bus={bus} station={station}></BusPopup>
                </Marker>)
              })
            }
            {lines.length > 0 && 
              lines.map((line, index) => {
                const pathOptions = {color: line.fields.couleurtrace};
                return(
                  <Polyline id={index} pathOptions={pathOptions} positions={line.fields.parcours.coordinates}>
                    <Tooltip onMouseOver={e => getCurrentLatLon(e)}><h2>Ligne {line.fields.nomcourtligne}</h2></Tooltip>
                  </Polyline>
                )
              })
            }
          </MapContainer>
        </div>
        <MapLegend lines={lines} network={station.network}/>
      </div>
    )
}


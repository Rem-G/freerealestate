
import React, { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import 'leaflet/dist/leaflet.css';

function ChangeView({center, zoom}) {
    if (center == [48.864716, 2.349014]){ zoom = 7 }
    const map = useMap();
    map.setView(center, zoom);
    return null;
  } 

export default function Map({station}){
    const position = [48.864716, 2.349014];
    return(
      <MapContainer center={position} zoom={7} scrollWheelZoom={false} style={{ height: "100%", width: "auto" }}>
          {station &&
            <ChangeView center={[station.lon, station.lat]} zoom={17}/>
          }
        <TileLayer
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={position}>
          <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
          </Popup>
        </Marker>
      </MapContainer>
    )

}


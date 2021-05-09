import { Popup } from 'react-leaflet'
import React from "react";
import TransportImage from "./transportImage";
import "../style/buspopup.css";

export default function BusPopup({bus, station}){
    return (
        <Popup maxHeight="10px">
            <div className="bus-popup">
                <TransportImage transport={bus.fields.nomcourtligne} network={station.network} width={"20px"} height={"20px"}></TransportImage>
                <h3>{bus.fields.destination}</h3>
            </div>
        </Popup>
    )
}
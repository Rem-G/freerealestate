import { Popup } from 'react-leaflet'
import React, { useEffect, useState } from "react";
import axios from "axios";
import "../style/buspopup.css";

export default function BusPopup({bus, station}){
    const [image, updateImage] = useState([])

    const fetchResults = () => {
		axios
		.get('http://localhost:8000/api/transport/getimage/'+bus.fields.nomcourtligne+'/'+station.network)
        .then(response => {
            updateImage("data:image/png;base64,"+response.data.ctx.image)
        }
        )
		.catch(err => {console.log(err);});
	};

	useEffect(() => {
		fetchResults();
        console.log(bus);
	}, [station]);


    return (
        <Popup maxHeight="10px">
            <div className="bus-popup">
                <img style={{height:"20px", width:"20px"}}src={image}/> <h3>{bus.fields.destination}</h3>
            </div>
        </Popup>
    )

}
import React, { useEffect, useState } from "react";
import axios from "axios";

export default function TransportImage({transport, network}){
    const [image, updateImage] = useState([])

    const fetchResults = () => {
        axios
        .get('http://localhost:8000/api/transport/getimage/'+transport+'/'+network)
        .then(response => {
            updateImage("data:image/png;base64,"+response.data.ctx.image)
        }
        )
        .catch(err => {console.log(err);});
    };

    useEffect(() => {
        fetchResults();
    }, [transport])

    return (
        <img style={{height:"20px", width:"20px", position:"relative"}}src={image}/>
    )
}

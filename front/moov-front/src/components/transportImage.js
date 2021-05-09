import React, { useEffect, useState } from "react";
import axios from "axios";

export default function TransportImage({transport, network, width, height, position, top, webkitTransform}){
    const [image, updateImage] = useState([])

    const fetchResults = () => {
        axios
        .get('http://localhost:8000/api/transport/getimage/'+transport+'/'+network)
        .then(response => {
            if (response.data.ctx.type === "png"){
                updateImage("data:image/png;base64,"+response.data.ctx.image);
            }
            else if (response.data.ctx.type === "svg"){
                updateImage(response.data.ctx.image);
            }
        }
        )
        .catch(err => {console.log(err);});
    };

    useEffect(() => {
        fetchResults();
    }, [transport])

    return (<img style={{height:height, width:width, position:position, top:top, webkitTransform:webkitTransform}}src={image}/>)

}

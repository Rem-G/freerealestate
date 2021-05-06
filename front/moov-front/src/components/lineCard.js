import React, { useEffect, useState } from "react";
import "../style/lineCard.css";
import axios from 'axios';

function LineCard({line, station}){
    const [image, updateImage] = useState([]);


    const fetchResults = () => {
		axios
		.get('http://localhost:8000/api/transport/getimage/'+line.line+'/'+station.network)
        .then(response => {
            updateImage("data:image/png;base64,"+response.data.ctx.image)
        }
        )
		.catch(err => {console.log(err);});
	};

	useEffect(() => {
		fetchResults();
	}, [line, station])

	return (
		<>
			<div className="result-text-wrapper">
				<div className="one">
					{image.length > 0 &&
						<img style={{height:"30px", width:"30px", top:"50%", webkitTransform: "translate(0%, 50%)"}} src={image}/>
					}
				</div>
				<div className="two">
					<span className="direction">{line.destination}</span>
				</div>
				<div className="three">
					<ul className="horaires">
						<li className="premierHoraire">{line.next_departures[0]}</li>
						<li className="deuxiemeHoraire">{line.next_departures[1]}</li>
						<li className="troisiemeHoraire">{line.next_departures[2]}</li>
					</ul>
				</div>
			</div>
			<div style={{height:"10px"}}></div>
		</>

		)
}

export default LineCard;
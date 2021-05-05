import React, { useEffect, useState } from "react";
import "../style/lineCard.css";
import axios from 'axios';

function LineCard({line, station}){
    const [image, updateImage] = useState([])

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

	///////////////////////////////////////
	// PENSER A METTRE A JOUR LES IMAGES //
	///////////////////////////////////////

	return (
		<div className="container">
			<div className="result">
				<img style={{height:"30px", width:"30px"}}src={image}/>
				{line.map((dest, index) => {
					console.log(dest);
					return (
					<>
					<span className="direction">{dest}</span>
					<div className="horaires">
						<span>{dest.next_departures[0]}</span>
						<span>{dest.next_departures[1]}</span>
						<span>{dest.next_departures[2]}</span>
					</div>
					</>)
				})}
			</div>
		</div>
		)
}

export default LineCard;
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

	// const LineImage = ({ data }) => <img src={`data:image/jpeg;base64,${data}`} />

	return (
		<div className="container">
			<div className="result">
				<img style={{height:"30px", width:"30px"}}src={image}/>
				<span className="direction">{line.destination}</span>
				<div className="horaires">
					<span>{line.next_departure}</span>
					{/* <h4>{line.next_departure.get(1)}</h4>
					<h4>{line.next_departure.get(2)}</h4> */}
				</div>
			</div>
		</div>
		)
}

export default LineCard;
import React, { useEffect, useState } from "react";
import "../style/lineCard.css";
import axios from 'axios';
import FreqChart from "./freqChart";

function LineCard({line, station}){
    const [image, updateImage] = useState([]);
	const [gif, updateGif] = useState();
	const [statPanel, updateStatPanel] = useState(false);

	function click() {
		if(statPanel == true) {
			updateStatPanel(false); 
		}
		else {
			updateStatPanel(true);
		}
	}

	const fetchGif = () => {
		axios
		.get('http://localhost:8000/api/transport/getgif/')
		.then(response => {
			updateGif("data:gif/gif;base64,"+response.data.ctx.gif)
		})
	};

	useEffect(() => {
		fetchGif();
	})

    const fetchResults = () => {
		axios
		.get('http://localhost:8000/api/transport/getimage/'+line.line+'/'+station.network)
        .then(response => {
            updateImage("data:image/png;base64,"+response.data.ctx.image)
        })
		.catch(err => {console.log(err);});
	};

	useEffect(() => {
		fetchResults();
	}, [line, station])

	return (
		<>
			<div className="result-text-wrapper" onClick={e => click()}>
				<div className="one">
					{image.length > 0 &&
						<img style={{height:"30px", width:"30px", top:"50%", webkitTransform: "translate(0%, 50%)"}} src={image}/>
					}
				</div>
				<div className="two">
					<span className="direction">{line.destination}</span>
				</div>
				<img className="gif" src={gif} style={{float:"left"}}></img>
				<div className="three">
					<ul className="horaires">
						<li className="premierHoraire">{line.next_departures[0]}</li>
						<li className="deuxiemeHoraire">{line.next_departures[1]}</li>
						<li className="troisiemeHoraire">{line.next_departures[2]}</li>
					</ul>
				</div>
			</div>
			<div style={{height:"10px"}}></div>
			{statPanel && 
					<div className="statPanel">
						<div className="premiereStat">
							<h5>Fréquentation de la ligne</h5>
							<FreqChart station={station} line={line.line} />
						</div>
					</div>
			}
		</>

		)
}

export default LineCard;
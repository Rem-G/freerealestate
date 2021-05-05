import React, { useEffect, useState } from "react";
import axios from "axios";
import LineCard from "./lineCard";
import "../style/timeTablePanel.css";

function TimeTablePanel({station}){
    const [lines, updateLines] = useState([])

    const fetchResults = () => {
		axios
		.get('http://127.0.0.1:8000/api/transport/nextdeparture/'+station.station+"/"+station.network)
        .then(response => {
            updateLines(response.data.next_departures);
			console.log(response.data.next_departures);
        }
        )
		.catch(err => {console.log(err);});
	};

	useEffect(() => {
		fetchResults()
		console.log(lines);
	}, [station]);

	return (
		<div className="panel">
			{lines.length > 0 &&
			Object.keys(lines).forEach((line) => {
				console.log(line);
				Object.keys(lines.line).forEach((dest) => {
					console.log(dest);
					return (<LineCard line={line} station={station}/>)
				})
			})}
			{lines.length == 0 &&
				<span className="empty">Pas de station selectionnée</span>
			}
		</div>
		)
}

export default TimeTablePanel;
import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";
import LineCard from "./lineCard";
import "../style/timeTablePanel.css";

function TimeTablePanel({station}){
    const [lines, updateLines] = useState([])

    async function fetchResults() {
		axios
		.get('http://localhost:8000/api/transport/nextdeparture/'+station.station+"/"+station.network)
        .then(response => {
            updateLines(response.data.next_departures);
			console.log(response.data.next_departures);
        }
        )
		.catch(err => {console.log(err);});
	};

	useEffect(() => {
		fetchResults();
		console.log(lines);
	}, [station]);

	return (
		<div className="panel">
			{lines.length > 0 &&
				lines.map((line, index ) => <LineCard line={line} station={station}/>)
			}
			{lines.length == 0 &&
				<span className="empty">Pas de station selectionnée</span>
			}
		</div>
		)
}

export default TimeTablePanel;
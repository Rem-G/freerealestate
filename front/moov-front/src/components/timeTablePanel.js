import React, { useEffect, useState } from "react";
import axios from "axios";
import LineCard from "./lineCard";
import "../style/timeTablePanel.css";

function TimeTablePanel({station, loaded, updateLoaded}){
    const [lines, updateLines] = useState([])

    async function fetchResults() {
		axios
		.get('https://moov-api.herokuapp.com/api/transport/nextdepartures/'+station.station+"/"+station.network)
        .then(response => {
            updateLines(response.data.next_departures);
			updateLoaded(loaded.add("nextdepartures"));
        	}
        )
		.catch(err => {console.log(err);});
	};

	useEffect(() => {
		fetchResults();
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
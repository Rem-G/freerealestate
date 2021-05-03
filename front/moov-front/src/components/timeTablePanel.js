import React, { useEffect, useState } from "react";
import axios from "axios";
import LineCard from "./lineCard"

function TimeTablePanel({station}){
    const [lines, updateLines] = useState([])

    const fetchResults = () => {
		axios
		.get('http://127.0.0.1:8000/api/transport/nextdeparture/'+station.station)
        .then(response => {
            lines.updateLines(response.line)
        }
        )
		.catch(err => {console.log(err);});
	};

	useEffect(() => {
		fetchResults()
	  }, [station]);

	return (
		<div className="panel">
			<div className="panel-results">
			{lines.map((line, index) =>(
                <LineCard line/>
				))
			}
			</div>
		</div>
		)
}

export default TimeTablePanel;
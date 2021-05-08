import React, { useEffect, useState} from 'react';
import SearchBar from './searchbar';
import Map from './map';
import TimeTablePanel from './timeTablePanel';
import Alert from './alert'
import Loader from "react-loader-spinner";
import "../style/transport.css";
import "../style/loader.css";

function Load(){
	return (
		<div className="loader-background">
			<div className="loader">
				<Loader
					type="Bars"
					color="rgba(236, 106, 92, 0.7)"
				/>
			</div>
		</div>
	)
}

export default function Transport({loaded, updateLoaded, station, updateStation, searchReq, updateSearchReq}){

	return(
		<div>
			{loaded.size < 1 && station !== "" &&
				<Load/>
			}
			<Alert station={station}></Alert>
			<SearchBar station={station} updateStation={updateStation} searchReq={searchReq} updateSearchReq={updateSearchReq} updateLoaded={updateLoaded}/>
			<div className="r1 c1">
				<Map station={station} loaded={loaded} updateLoaded={updateLoaded}/>
			</div>
			<div classname="side panel">
				<TimeTablePanel station={station} loaded={loaded} updateLoaded={updateLoaded}/>
			</div>
		</div>
	);
};
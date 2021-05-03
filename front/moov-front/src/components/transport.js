import React, {useState} from 'react';
import SearchBar from './searchbar';
import Map from './map';
import TimeTablePanel from './timeTablePanel';
import "../style/transport.css";
import "../style/map.css";

export default function Transport({station, updateStation, searchReq, updateSearchReq}){

	React.useEffect(() => {

	// eslint-disable-next-line
	}, [searchReq], );

	return(
		<div >
			<SearchBar station={station} updateStation={updateStation} searchReq={searchReq} updateSearchReq={updateSearchReq}/>
			<div className="map r1 c1">
				<Map station={station}/>
			</div>
			<div classname="side panel">
				<TimeTablePanel station={station}/>
			</div>
		</div>
	);
};
import React from 'react';
import SearchBar from './searchbar';
import Map from './map';
import "../style/transport.css";
import "../style/map.css";

export default function Transport({station, updateStation, searchReq, updateSearchReq}){
	return(
		<div >
			<SearchBar station={station} updateStation={updateStation} searchReq={searchReq} updateSearchReq={updateSearchReq}/>
			<div className="map r1 c1">
				<Map station={station}/>
			</div>
		</div>
	);
};
import React, {useState} from 'react';
import SearchBar from './searchbar';
import Map from './map';
import "../style/transport.css";
import "../style/map.css";

export default function Transport({station, updateStation, searchReq, updateSearchReq}){

	React.useEffect(() => {

	// eslint-disable-next-line
	}, [searchReq], );

	return(
		<div >
			<SearchBar searchReq={searchReq} updateSearchReq={updateSearchReq}/>
			<div className="map r1 c1">
				<Map/>
			</div>
		</div>
	);
};
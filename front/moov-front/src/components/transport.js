import React, {useState} from 'react';
import SearchBar from './searchbar';
import "../style/transport.css";

export default function Transport({station, updateStation, searchReq, updateSearchReq}){

	React.useEffect(() => {

	// eslint-disable-next-line
	}, [searchReq], );

	return(
		<div >
			<SearchBar searchReq={searchReq} updateSearchReq={updateSearchReq}/>
		</div>
	);
};
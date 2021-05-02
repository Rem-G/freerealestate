import React, {useState} from 'react';
import axios from "axios";
import "../style/searchbar.css";

function SearchBar({station, updateStation}){
    const [suggestions, updateSuggestions] = useState([])

	//replace with findStation
    const onChangeHandler = event => {
        axios
			.get(`http://127.0.0.1:8000/api/transport/findstation/${event.target.value}`)
			.then(response => {
				updateSuggestions(response.data.network);
			}) 
			.catch(err => {console.log(err); updateSuggestions([])});
	  };

	//replace with exact station, do not require to make forEach
	const fetchStation = (req_station) => {

		axios
		.get('http://127.0.0.1:8000/api/transport/station/'+req_station)
		.then(response => {
			response.data.network.forEach(element => {
				if (element.station == req_station) { updateStation(element); }
			});
		})
		.catch(err => {console.log(err);});
	};

	const handleSubmit = event => {
		const res = event.target.textContent.split(' - ');
		res.pop();
		const req_station = res[0];
		updateSuggestions([]);
		fetchStation(req_station);
	};

	return (
		<div className="searchbar">
			<div className="search-box searchbar">
				<input type="text" name="" className="search-txt" placeholder="Trouver une station" onChange={onChangeHandler}/>
			</div>
			<div className="searchbar-results">
			{suggestions.map((suggestion, index) =>(
				<div className="searchbar-result-box" onClick={handleSubmit}>{suggestion.station} - {suggestion.network}</div>
				))
			}
			</div>
		</div>
		)
}

export default SearchBar;
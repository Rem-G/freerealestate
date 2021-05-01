import React, {useState} from 'react';
import "../style/searchbar.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faGreaterThan } from '@fortawesome/free-solid-svg-icons'
import axios from "axios";

function SearchBar({searchReq, updateSearchReq}){
    const [suggestions, updateSuggestions] = useState([])

    const onChangeHandler = event => {
        axios
			.get(`http://127.0.0.1:8000/api/transport/station/${event.target.value}`)
			.then(response => {
				let tempData = [];
				if(response.data.network.length > 5){
					for (let i = 0; i < 5; i++){
						tempData.push(response.data.network[i]);
					}
					updateSuggestions(response.data.network);
				}
				else{
					updateSuggestions(response.data.network);
				}

			}) 
			.catch(err => {console.log(err); updateSuggestions([])});
	  };

	const handleSubmit = event => {
		const res = event.target.textContent.split(' ');
		res.pop();
		updateSearchReq(res.join(' '));
		updateSuggestions([]);
	};

	const handleKeyDown = (e) => {
		if (e.key === 'Enter') {
			handleSubmit(e);
		 }
	}

	return (
		<div className="searchbar">
			<div className="search-box searchbar">
				<input type="text" name="" className="search-txt" placeholder="Trouver une station" onChange={onChangeHandler} onKeyDown={handleKeyDown}/>
				<FontAwesomeIcon className="search-btn" icon={faGreaterThan} onClick={handleSubmit} />
			</div>
			<div className="searchbar-results">
			{suggestions.map((suggestion, index) =>(
				<div className="searchbar-result-box" onClick={handleSubmit}>{suggestion.station} <span className="searchbar-span-network">{suggestion.network}</span></div>
				))
			}
			</div>
		</div>
		)
}

export default SearchBar;
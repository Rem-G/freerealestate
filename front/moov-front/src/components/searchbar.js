import React, {useState} from 'react';
import "../style/searchbar.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faGreaterThan } from '@fortawesome/free-solid-svg-icons'
import axios from "axios";

function SearchBar({searchReq, updateSearchReq}){
	const [tempCity, setTempCity] = useState("");
    const [suggestions, updateSuggestions] = useState([])

    const onChangeHandler = event => {
        axios
			.get("http://127.0.0.1:8000/api/transport/station/"+event.target.value)
			.then(response => {
                updateSuggestions(response.data.network);
			}) // you have array in your response.data so add your data here
			.catch(err => console.log(err));
	  };

	const handleSubmit = () => {
		updateSearchReq(tempCity);
	};

	const handleKeyDown = (e) => {
		if (e.key === 'Enter') {
			handleSubmit();
		 }
	}

	return (
		<div className="searchbar">
			<div className="search-box searchbar">
				<input type="text" name="" className="search-txt" placeholder="Trouver une station" onChange={onChangeHandler} onKeyDown={handleKeyDown}/>
				<FontAwesomeIcon className="search-btn" icon={faGreaterThan} onClick={handleSubmit} />
			</div>
            <ul>
                {suggestions.map((suggestion, index) =>(
                    <li>{suggestion.station} - {suggestion.network}</li>
                    ))
                }
            </ul>
		</div>
	)
}

export default SearchBar;
import React, { useEffect, useState } from "react";
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import '../style/alert.css'
import axios from "axios";
import RecipeReviewCard from './alert_card'
import WarningIcon from '@material-ui/icons/Warning';


export default function Alert ({station}) {

    const [alertes, update_alerte] = useState({})
    function isKeyExists(obj,key){
        if(obj[key] == undefined ){
            return false;
        }
        return true;
    }
    const fetchResults = () => {
		axios
		.get('http://127.0.0.1:8000/api/transport/alert/'+ station.network  + "/" + "all/2")
        .then(response => {
            update_alerte(response.data.alert)
        }
        )
		.catch(err => {console.log(err);});
	};

	useEffect(() => {
		fetchResults()
	  }, [station]);

    if (isKeyExists(alertes, 'BUS')) {
    return(
    <div className= "alert_panel">
    <Popup trigger={<WarningIcon style={{ fontSize: 40 }}></WarningIcon>} position="center">
    <div className = "pop_up">
        <h2>Information résaux</h2>

        {/* Visualisaton des Metro */}
        <div className= "metro_tram_bus">
        <h3 className = "back">Alerte Metro</h3>
        {alertes.METRO.length > 0 ?
        alertes.METRO.map(alerte =>
        <div className = "card_div">
        <RecipeReviewCard ligne = {alerte.ligne_cli}  date = {alerte.debut} titre = {alerte.titre} message = {alerte.message}/>
        </div>
        )
        :
        "Aucune alerte réseaux"
        }
        </div>


        {/* Visualisaton des TRAM */}
        <div className= "metro_tram_bus">
        <h3 className = "back" >Alerte TRAM</h3>
        {alertes.TRAM.length > 0 ?
        alertes.TRAM.map(alerte =>
        <div className = "card_div">
        <RecipeReviewCard ligne = {alerte.ligne_cli}  date = {alerte.debut} titre = {alerte.titre} message = {alerte.message}/>
        </div>
        )
        :
        "Aucune alerte réseaux"
        }
        </div>

        {/* Visualisaton des BUS */}
        <div className= "metro_tram_bus">
        <h3 className = "back">Alerte BUS</h3>
        {alertes.BUS.length > 0 ?
        alertes.BUS.map(alerte =>
        <div className = "card_div">
        <RecipeReviewCard ligne = {alerte.ligne_cli}  date = {alerte.debut} titre = {alerte.titre} message = {alerte.message}/>
        </div>
        )
        :
        "Aucune alerte réseaux"
        }

        </div>
    </div>
    </Popup>
    </div>
    )
    }
    else return(
        <div>
        </div>
    )
}

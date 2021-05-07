import React, { useEffect, useState } from "react";
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import '../style/alert.css'
import axios from "axios";
import RecipeReviewCard from './alert_card'
import WarningIcon from '@material-ui/icons/Warning';
import { TwitterTimelineEmbed, TwitterShareButton, TwitterFollowButton, TwitterHashtagButton, TwitterMentionButton, TwitterTweetEmbed, TwitterMomentShare, TwitterDMButton, TwitterVideoEmbed, TwitterOnAirButton } from 'react-twitter-embed';


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

            {alertes.METRO.length > 0 && <div>
            <div className= "metro_tram_bus">
            <h3 className = "back">Alerte Metro</h3>
            {alertes.METRO.map(alerte =>
            <div className = "card_div">
            <RecipeReviewCard ligne = {alerte.ligne_cli}  date = {alerte.debut} titre = {alerte.titre} message = {alerte.message}/>
            </div>
            )
            }
            </div>
            </div>
            }

            {alertes.TRAM.length > 0 && <div>
            <div className= "metro_tram_bus">
            <h3 className = "back">Alerte tram</h3>
            {alertes.TRAM.map(alerte =>
            <div className = "card_div">
            <RecipeReviewCard ligne = {alerte.ligne_cli}  date = {alerte.debut} titre = {alerte.titre} message = {alerte.message}/>
            </div>
            )
            }
            </div>
            </div>
            }

            {alertes.BUS.length > 0 && <div>
            <div className= "metro_tram_bus">
            <h3 className = "back">Alerte bus</h3>
            {alertes.BUS.map(alerte =>
            <div className = "card_div">
            <RecipeReviewCard ligne = {alerte.ligne_cli}  date = {alerte.debut} titre = {alerte.titre} message = {alerte.message}/>
            </div>
            )
            }
            </div>
            </div>
            }
    </div>
    </Popup>
    </div>
    )
    }

    if (station.network === "Lille") {
    return(
        <div className= "alert_panel">
        <Popup trigger={<WarningIcon style={{ fontSize: 40 }}></WarningIcon>} position="center">
        <div className = "pop_up">
        <h3>Metro</h3>
        <TwitterTimelineEmbed
            sourceType="profile"
            screenName="ilevia_metro"
            options={{height: 700}}
        />

        <h3>Tram</h3>
        <TwitterTimelineEmbed
            sourceType="profile"
            screenName="ilevia_tram"
            options={{height: 700}}
        />

        <h3>Bus</h3>
        <TwitterTimelineEmbed
            sourceType="profile"
            screenName="ilevia_bus"
            options={{height: 700}}
        />
        </div>
        </Popup>
        </div>
    )
    }
    else {
        return(<></>)
    }
}

import React, { useEffect, useState } from "react";
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import '../style/alert.css'
import axios from "axios";
import AlertCard from './alertCard'
import WarningIcon from '@material-ui/icons/Warning';
import { TwitterTimelineEmbed } from 'react-twitter-embed';
import { Button } from "@material-ui/core";


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
    <Popup trigger={<Button style={{ fontSize: "10px", borderRadius:"5px", padding: "15px", textAlign: "center", width: "100%" }}>Informations réseau</Button>} position="center">
    <div className = "pop_up">
        <h2>Informations réseau</h2>

        {/* Visualisaton des Metro */}

            {alertes.METRO.length > 0 && <div>
            <div className= "metro_tram_bus">
            <h3 className = "back">Métro</h3>
            {alertes.METRO.map(alerte =>
                <div className="alertWrapper">
                    <AlertCard ligne = {alerte.ligne_cli}  date = {alerte.debut} titre = {alerte.titre} message = {alerte.message} station={station}/>
                </div>
            )
            }
            </div>
            </div>
            }

            {alertes.TRAM.length > 0 && <div>
            <div className= "metro_tram_bus">
            <h3 className = "back">Tramway</h3>
            {alertes.TRAM.map(alerte =>
                <div className="alertWrapper">
                <AlertCard ligne = {alerte.ligne_cli}  date = {alerte.debut} titre = {alerte.titre} message = {alerte.message} station={station}/>
                </div>
            )
            }
            </div>
            </div>
            }

            {alertes.BUS.length > 0 && <div>
            <div className= "metro_tram_bus">
            <h3 className = "back">Bus</h3>
            {alertes.BUS.map(alerte =>
                <div className = "alertWrapper">
                    <AlertCard ligne = {alerte.ligne_cli}  date = {alerte.debut} titre = {alerte.titre} message = {alerte.message} station={station}/>
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

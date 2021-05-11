import React, { useEffect, useState } from "react";
import Popup from 'reactjs-popup';
import axios from "axios";
import AlertCard from './alertCard'
import WarningIcon from '@material-ui/icons/Warning';
import { TwitterTimelineEmbed } from 'react-twitter-embed';
import { Button } from "@material-ui/core";
import '../style/alert.css'

export default function Alert ({station}) {
    const [alertes, update_alerte] = useState({});
    const [openPanel, updateOpenPanel] = useState(false);

    const handleOpenPanel = () => { updateOpenPanel(!openPanel); }

    function isKeyExists(obj,key){
        if(obj[key] == undefined ){
            return false;
        }
        return true;
    }
    const fetchResults = () => {
		axios
		.get('https://moov-api.herokuapp.com/api/transport/alert/'+ station.network  + "/" + "all/2")
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
        <>
        <button className="alert-button" onClick={handleOpenPanel}>Informations</button>
        {openPanel &&
            <div className= "alert_panel">
                <div className = "pop_up">
                    <h2>Informations réseau</h2>

                    {/* Visualisaton des Metro */}

                    {alertes.METRO.length > 0 && 
                        <div className= "metro_tram_bus">
                            <h3 className = "back">Métro</h3>
                            {alertes.METRO.map(alerte =>
                                <div className="alertWrapper">
                                    <AlertCard ligne = {alerte.ligne_cli}  date = {alerte.debut} titre = {alerte.titre} message = {alerte.message} station={station}/>
                                </div>
                            )}
                        </div>
                    }

                    {alertes.TRAM.length > 0 &&
                        <div className= "metro_tram_bus">
                            <h3 className = "back">Tramway</h3>
                            {alertes.TRAM.map(alerte =>
                                <div className="alertWrapper">
                                    <AlertCard ligne = {alerte.ligne_cli}  date = {alerte.debut} titre = {alerte.titre} message = {alerte.message} station={station}/>
                                </div>
                            )}
                        </div>
                    }

                    {alertes.BUS.length > 0 &&
                        <div className= "metro_tram_bus">
                            <h3 className = "back">Bus</h3>
                            {alertes.BUS.map(alerte =>
                                <div className="alertWrapper">
                                    <AlertCard ligne = {alerte.ligne_cli}  date = {alerte.debut} titre = {alerte.titre} message = {alerte.message} station={station}/>
                                </div>
                            )}
                        </div>
                    }
                </div>
            </div>
        }
    </>
    )}

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

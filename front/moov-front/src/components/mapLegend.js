import React, { useEffect, useState} from "react";
import "../style/maplegend.css"
import TransportImage from "./transportImage";

export default function MapLegend({lines, network}) {
    const [legendLines, updateLegendLines] = useState([]);

    useEffect(() => {
        filterLegend();
    }, [lines]);

    const filterLegend = () => {
        let insertedLines = [];
        let insertedLinesObj = [];
        lines.forEach(line => {
            if (!insertedLines.includes(line.fields.nomcourtligne)){
                insertedLines.push(line.fields.nomcourtligne);
                insertedLinesObj.push(line);
            }
        });
        updateLegendLines(insertedLinesObj);
    }

    return (
        <div className="legend-card">
            <p style={{fontSize: " .83em", fontWeight: "bolder", paddingBottom: "10px"}} >Légende</p>
            {legendLines.map((line) =>
                <div className="legend-card-row">
                    <div className="legend-card-column" style={{width: "30px"}}>
                        <TransportImage transport={line.fields.nomcourtligne} network={network}></TransportImage>
                    </div>
                    <div className="legend-card-column" style={{background: line.fields.couleurtrace, width:"15px", height:"4px", top:"50%"}}></div>
                </div>
            )}
        </div>
    )
}
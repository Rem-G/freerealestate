import React, { useEffect, useState} from "react";
import "../style/maplegend.css"
import TransportImage from "./transportImage";

export default function MapLegend({lines, station}) {
    const [legendLines, updateLegendLines] = useState([]);

    useEffect(() => {
        updateLegendLines([]);
    }, [station]);

    useEffect(() => {
        filterLegend();
        console.log(lines);
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
            <p style={{fontSize: " .83em", paddingBottom: "10px", textAlign: "center"}} >Lignes</p>
            {legendLines.map((line) =>
                <div className="legend-card-row">
                    <div className="legend-card-column" style={{width: "30px"}}>
                        <TransportImage transport={line.fields.nomcourtligne} network={station.network} width={"20px"} height={"20px"} position={"relative"}></TransportImage>
                    </div>
                    <div className="legend-card-column" style={{background: line.fields.couleurtrace, width:"15px", height:"4px", top:"50%"}}></div>
                </div>
            )}
        </div>
    )
}
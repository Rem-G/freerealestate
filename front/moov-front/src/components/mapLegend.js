import React, { useEffect, useState} from "react";
import "../style/maplegend.css"

export default function MapLegend({lines}) {
    const [legendLines, updateLegendLines] = useState([]);

    useEffect(() => {
        console.log(lines);
        filterLegend();
    }, [lines]);

    const filterLegend = () => {
        let insertedLines = [];
        lines.forEach(line => {
            if (!insertedLines.includes(line.fields.nomcourtligne)){
                insertedLines.push(line.fields.nomcourtligne);
            }
        });
        updateLegendLines(insertedLines);
    }

    return (
        <div className="legend-card">
            {legendLines.map((line) => <span>{line}</span>)}
        </div>
    )
}
import React, { useEffect, useState } from "react";
import axios from "axios";

function LineCard({line}){

	return (
		<div className="result">
            <h2 className="line">{line.line}</h2>
			<h3 className="direction">{line.direction}</h3>
			<div className="horraires">
				<h2>{line.horraire.get(0)}</h2>
				<h4>{line.horraire.get(1)}</h4>
				<h4>{line.horraire.get(2)}</h4>
			</div>
		</div>
		)
}

export default LineCard;
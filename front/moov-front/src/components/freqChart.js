import axios from 'axios';
import React, { useState, useEffect } from 'react'
import { Line } from 'react-chartjs-2'
import * as ChartAnnotation from '../utils/chartjs-plugin-annotation-0.5.7';

const FreqChart = ({station, line}) => {
    const [stationFreq, updateStationFreq] = useState({});
    const [data, updateData] = useState({});

    const fetchFreq = () => {
		axios
		.get('https://moov-api.herokuapp.com/api/transport/frequentation/'+line+'/'+station.network)
        .then(response => {
            updateStationFreq(response.data.frequentation);
            updateData({
                datasets: [
                {
                    label: 'number',
                    fill: true,
                    backgroundColor: "rgba(155, 205, 178, 0.5)",
                    data: response.data.frequentation.values,
                },
                ],
                labels: response.data.frequentation.labels,
            });
        }
        )
		.catch(err => {console.log(err);});
	};

    const datasetKeyProvider=()=>{
        return btoa(Math.random()).substring(0,12)
    }

    const ticksLabels = ["", "Faible", "Moyenne", "Haute"];

    const options = {
        responsive: true,
        scales: {
          xAxes: [{
              gridLines: {
                  color: "rgba(0, 0, 0, 0)",
                  display: false,
              },
              ticks: {
                fontSize: 10,
                autoSkip: false
              }

          }],
          yAxes: [
            {
              position: 'left',
                gridLines: {
                    color: "rgba(0, 0, 0, 0)",
                    display: false,
                },
                ticks: {
                  // scaleShowValues: true,
                  autoSkip: false,
                    display: true,
                    beginAtZero: true,
                    callback: function(value, index, values) {
                        return ticksLabels[value];
                    }
                },
            },
          ],
        },
        elements: {
            point:{
                radius: 0
            }
        },
        legend: {
            display: false
         },
         tooltips: {
            enabled: false
         },
        annotation: {
            annotations: [
              {
                type: 'line',
                mode: 'vertical',
                scaleID: 'x-axis-0',
                value: stationFreq.current_index,
                borderColor: 'grey',
                borderWidth: 2,
              },
            ],
          },
        plugins: {
            legend: {
              boxWidth: "10px",
            },
            datalabels: {
              formatter: function(value, context) {
                return "";
              }
            }
          }
    }


  useEffect(() => {
    fetchFreq();
  // eslint-disable-next-line
  }, [line]);

  return (
        <Line data={data} options={options} datasetKeyProvider={datasetKeyProvider} plugins={ChartAnnotation} />
  )
}

export default FreqChart;

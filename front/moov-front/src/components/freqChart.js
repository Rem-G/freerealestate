import axios from 'axios';
import React, { useState, useEffect } from 'react'
import { Line } from 'react-chartjs-2'
import * as ChartAnnotation from '../utils/chartjs-plugin-annotation-0.5.7';


const FreqChart = ({station, line}) => {
    const [data, updateData] = useState({});

    const fetchFreq = () => {
		axios
		.get('http://localhost:8000/api/transport/frequentation/'+line+'/'+station.network)
        .then(response => {
            updateData(response.data);
        }
        )
		.catch(err => {console.log(err);});
	};

    const datasetKeyProvider=()=>{ 
        return btoa(Math.random()).substring(0,12)
    }

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
                  display: false,
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
                value: data.current_index,
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
    updateData({
        datasets: [
        {
            label: 'number',
            fill: true,
            backgroundColor: "rgba(243, 174, 98, 0.2)",
            data: data.values,
        },
        ],
        labels: data.labels,
    });
    
  // eslint-disable-next-line
  }, [line]);

  return (
      <Line data={data} options={options} datasetKeyProvider={datasetKeyProvider} plugins={ChartAnnotation} />
  )
}

export default FreqChart;

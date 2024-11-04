<template>
    <div>
      <h2>Sample data from FASTAPI</h2>
      <div ref="plotlyChart" style="width: 100%; height: 400px;"></div>
    </div>
  </template>
  <script>
  import Plotly from 'plotly.js-dist';
  import {fetchWeatherData} from '../utils/fetchWeatherData.js'
  export default {
    name: 'TestGraph',
    async mounted() {
        let temp_data = await fetchWeatherData();
        
        let x_data = [];
        let y_data = [];
        temp_data.data.forEach(point => {
            let date = new Date(point.timestamp * 1000);
            let year = date.getFullYear();
            let month = date.getMonth();
            let day = date.getDate();
            let formattedTime = 
            (day < 10 ? '0' : '') + day + '.' + 
            ((month + 1) < 10 ? '0' : '') + (month + 1) + '.' + 
            year;


            x_data.push(formattedTime)
            y_data.push(point.value)
        });
        const data = [
        {
            x: x_data,
            y: y_data,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Average Temp (°C)',
            marker: { color: 'red' },
            yaxis: 'y1',  
        },
       
        ];
        const layout = {
        title: 'Temperature and Humidity in Berlin (August 2015-2023)',
        xaxis: { title: 'Year' },
        yaxis: { title: 'Temperature (°C)', side: 'left', showgrid: false },
        yaxis2: {
            title: 'Humidity (%)',
            overlaying: 'y', 
            side: 'right',   
        },
        };
        Plotly.newPlot(this.$refs.plotlyChart, data, layout);
    },
  };
  </script>
  <style scoped>
  h2 {
    text-align: center;
    margin-bottom: 10px;
  }
  </style>
<template>
    <div>
      <h2>Mean Soil Temperature in August</h2>
  
      <!-- Plotly Chart -->
      <div ref="plotlyChart" style="width: 100%; height: 400px;"></div>
    </div>
  </template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Plotly from 'plotly.js-dist-min';

export default {
  name: 'MeanSoilTempGraph',
  setup() {
    const weatherData = ref(null);
    const plotData = ref([]);
    const plotlyChart = ref(null);

    const fetchData = async () => {
      const apiUrl = 'http://localhost:8000/weather/index';

      const params = {
        weatherVariable: "soil_temperature_0_to_7cm",
        startDate: new Date('2015-01-01').getTime() / 1000, // Fixed start date
        endDate: new Date('2023-12-31').getTime() / 1000, // Fixed end date
        location: "TEMPELHOFER_FELD",
        temporalResolution: "MONTHLY",
        aggregation: "MEAN",
      };

      try {
        const response = await axios.get(apiUrl, { params });
        weatherData.value = response.data;
        processData(response.data);
        renderPlot();
      } catch (error) {
        console.error("Error fetching temperature data:", error);
      }
    };

    const processData = (apiResponse) => {
      if (!apiResponse.data || !Array.isArray(apiResponse.data)) {
        console.log('Unexpected data format:', apiResponse);
        return;
      }

      // Filter for August data (month is 7 since JavaScript months are 0-indexed)
      const augustData = apiResponse.data.filter(entry => {
        const date = new Date(entry.timestamp * 1000);
        return date.getMonth() === 7; // August is month 7
      });

      // Extract years and temperatures for filtered data
      const years = augustData.map(entry =>
        new Date(entry.timestamp * 1000).getFullYear().toString()
      );
      const temperatures = augustData.map(entry => entry.value);

      // Update plot data
      plotData.value = [
        {
          x: years,
          y: temperatures,
          type: 'bar',
          name: 'August Soil Temperature',
          marker: { color: 'darkgreen' }
        }
      ];
    };

    const renderPlot = () => {
      const layout = {
        title: 'Mean Soil Temperature for Tempelhofer Feld (2015 - 2023)',
        xaxis: { title: 'Year', type: 'category' },
        yaxis: { title: 'Temperature (°C)' },
        template: 'plotly_white'
      };

      Plotly.newPlot(plotlyChart.value, plotData.value, layout);
    };

    onMounted(() => {
      fetchData();
    });

    return {
      weatherData,
      plotlyChart
    };
  }
};
</script>

<style scoped>
h2 {
  text-align: center;
  margin-bottom: 10px;
}
</style>
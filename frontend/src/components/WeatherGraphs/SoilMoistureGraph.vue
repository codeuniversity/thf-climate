<template>
    <div>
      <h2>Mean Monthly Soil Moisture</h2>
  
      <!-- Date Range Input Fields -->
      <div class="date-picker">
        <label>
          Start Date:
          <input type="date" v-model="startDate" @change="updateDateRange" />
        </label>
        <label>
          End Date:
          <input type="date" v-model="endDate" @change="updateDateRange" />
        </label>
      </div>
  
      <!-- Plotly Chart -->
      <div ref="plotlyChart" style="width: 100%; height: 400px;"></div>
  
    
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import Plotly from 'plotly.js-dist-min';
  
  export default {
    name: 'MeanSoilMoistureGraph',
    setup() {
      const weatherData = ref(null);
      const startDate = ref('2015-01-01');
      const endDate = ref('2023-12-31');
      const plotData = ref([]);
      const plotlyChart = ref(null);
  
      const fetchData = async () => {
        const apiUrl = 'https://thf-climate-run-1020174331409.europe-west3.run.app/weather/index';
  
        const params = {
          weatherVariable: "soil_temperature_0_to_7cm",
          startDate: new Date(startDate.value).getTime() / 1000,
          endDate: new Date(endDate.value).getTime() / 1000,
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
  
        const dates = apiResponse.data.map(entry =>
          new Date(entry.timestamp * 1000).toISOString().split('T')[0]
        );
        const temperatures = apiResponse.data.map(entry => entry.value);
  
        plotData.value = [
          {
            x: dates,
            y: temperatures,
            type: 'bar',
            name: 'Moisture',
            marker: { color: 'green' }
          }
        ];
      };
  
      const renderPlot = () => {
        const layout = {
          title: 'Mean Monthly Soil Moisture for Tempelhofer Feld (2015 - 2023)',
          xaxis: { title: '', type: 'date', rangeslider: { visible: true } },
          yaxis: { title: 'Moisture (m³/m³)' },
          template: 'plotly_white'
        };
  
        Plotly.newPlot(plotlyChart.value, plotData.value, layout);
      };
  
      const updateDateRange = () => {
        if (startDate.value && endDate.value) {
          fetchData();
        }
      };
  
      onMounted(() => {
        fetchData();
      });
  
      return {
        weatherData,
        startDate,
        endDate,
        updateDateRange,
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
  .date-picker {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  </style>
  
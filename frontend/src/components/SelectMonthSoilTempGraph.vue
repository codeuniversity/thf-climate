<template>
    <div>
      <h2>Mean Soil Temperature by Month</h2>
  
      <!-- Month Picker -->
      <div class="date-picker">
        
        <label>
         Select Month:
          <select v-model="selectedMonth" @change="updateGraph">
            <option v-for="(month, index) in months" :key="index" :value="index">
              {{ month }}
            </option>
          </select>
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
  name: 'SelectMonthMeanSoilTempGraph',
  setup() {
    const weatherData = ref(null);
    const startDate = ref('2015-01-01');
    const endDate = ref('2023-12-31');
    const selectedMonth = ref(0); // Default to January (0-indexed)
    const months = ref([
      'January', 'February', 'March', 'April', 'May', 
      'June', 'July', 'August', 'September', 
      'October', 'November', 'December'
    ]);
    const plotData = ref([]);
    const plotlyChart = ref(null);

    const fetchData = async () => {
      const apiUrl = 'http://localhost:8000/weather/index';

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

      // Filter for the selected month
      const filteredData = apiResponse.data.filter(entry => {
        const date = new Date(entry.timestamp * 1000);
        return date.getMonth() === selectedMonth.value;
      });

      // Extract years and temperatures for the filtered data
      const years = filteredData.map(entry =>
        new Date(entry.timestamp * 1000).getFullYear().toString()
      );
      const temperatures = filteredData.map(entry => entry.value);

      // Update plot data
      plotData.value = [
        {
          x: years,
          y: temperatures,
          type: 'bar',
          name: months.value[selectedMonth.value],
          marker: { color: 'darkgreen' }
        }
      ];
    };

    const renderPlot = () => {
      const layout = {
        title: `Mean Soil Temperature in ${months.value[selectedMonth.value]} for Tempelhofer Feld`,
        xaxis: { title: 'Year', type: 'category' },
        yaxis: { title: 'Temperature (°C)' },
        template: 'plotly_white'
      };

      Plotly.newPlot(plotlyChart.value, plotData.value, layout);
    };

    const updateGraph = () => {
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
      selectedMonth,
      months,
      updateGraph,
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

p {
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

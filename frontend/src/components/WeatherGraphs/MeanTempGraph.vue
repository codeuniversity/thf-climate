<template>
  <div>
    <!-- Date Range Input Fields -->
    <!-- 
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
    -->

    <!-- Plotly Chart -->
    <div ref="plotlyChart" style="width: 100%; height: auto"></div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import Plotly from "plotly.js-dist-min";

export default {
  name: "MeanTempGraph",
  setup() {
    // Constants for location and data configuration
    const location = ref("TEMPELHOFER_FELD"); 
    const temporalResolution = ref("MONTHLY"); 
    const aggregation = ref("MEAN"); 
    const temperatureData = ref(null);
    const startDate = ref("1990-01-01"); 
    const endDate = ref("2024-11-30"); 
    const plotData = ref([]); 
    const plotlyChart = ref(null); 
    
    // Fetches temperature data from the weather API.
    const fetchTemperatureData = async () => {
      const apiUrl = "https://thf-climate-run-1020174331409.europe-west3.run.app/weather/index";
      
      const params = {
        weatherVariable: "temperature_2m",
        startDate: new Date(startDate.value).getTime() / 1000,
        endDate: new Date(endDate.value).getTime() / 1000,
        location: location.value,
        temporalResolution: temporalResolution.value,
        aggregation: aggregation.value,
      };

      try {
        const response = await axios.get(apiUrl, { params });
        temperatureData.value = response.data;
        processData(response.data);
        renderPlot();
      } catch (error) {
        console.error("Error fetching temperature data:", error);
      }
    };

   
    // Processes the API response into a suitable format for Plotly.
    const processData = (apiResponse) => {
      if (!apiResponse.data || !Array.isArray(apiResponse.data)) {
        console.log("Unexpected data format:", apiResponse);
        return;
      }

      // Extract dates and temperatures from response
      const dates = apiResponse.data.map(
        (entry) => new Date(entry.timestamp * 1000).toISOString().split("T")[0]
      );
      const temperatures = apiResponse.data.map((entry) => entry.value);

      // Update plot data with formatted data
      plotData.value = [
        {
          x: dates,
          y: temperatures,
          mode: "lines",
          name: "Temperature",
          line: { color: "#FF4136" },
        },
      ];
    };

    
     // Renders the Plotly chart using processed data.
    const renderPlot = () => {
      const layout = {
        title: "Mean Monthly Temperature (1990 - 2024)",
        xaxis: {
          title: "",
          type: "date",
          rangeslider: { visible: true }, 
        },
        yaxis: { title: "Temperature (°C)" },
        template: "plotly_white", 
      };

      Plotly.newPlot(plotlyChart.value, plotData.value, layout);
    };

   
    // Triggers data fetching when the date range is updated.
    const updateDateRange = () => {
      if (startDate.value && endDate.value) {
        fetchTemperatureData();
      }
    };

    // Fetch data on component mount
    onMounted(() => {
      fetchTemperatureData();
    });

    return {
      temperatureData,
      startDate,
      endDate,
      updateDateRange,
      plotlyChart,
    };
  },
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

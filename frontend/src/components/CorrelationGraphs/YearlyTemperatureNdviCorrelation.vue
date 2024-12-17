<template>
  <v-container>
    <!-- Main container for the plot -->
    <v-row justify="center">
      <div
        ref="plotContainer"
        class="d-flex justify-center plot-container"
      ></div>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import Plotly from "plotly.js-dist-min";
import { onMounted, ref, watch } from "vue";

export default {
  name: "YearlyNdviTemperaturePlot",
  setup() {
    // Constants for location and data configuration
    const location = ref("TEMPELHOFER_FELD"); 
    const temporalResolution = ref("MONTHLY");
    const aggregation = ref("MEAN"); 
    const startDate = ref(1514764800); // 2018-01-01 as Unix timestamp
    const endDate = ref(1733007599); // 2024-11-30 as Unix timestamp
    const temperatureData = ref(null); 
    const ndviData = ref(null); 
    const plotContainer = ref(null); // Reference to the container for the Plotly chart

    const fetchTemperatureData = async () => {
      const apiUrl = "https://thf-climate-run-1020174331409.europe-west3.run.app/weather/index";

      // Query parameters for the temperature API
      const params = {
        weatherVariable: "temperature_2m",
        startDate: startDate.value,
        endDate: endDate.value,
        location: location.value,
        temporalResolution: temporalResolution.value,
        aggregation: aggregation.value,
      };

      try {
        const response = await axios.get(apiUrl, { params });
        temperatureData.value = response.data; // Store the response in a reactive variable
      } catch (error) {
        console.error("Error fetching temperature data:", error);
      }
    };

    
    const fetchNdviData = async () => {
      const apiUrl = "https://thf-climate-run-1020174331409.europe-west3.run.app/index/ndvi";

      // Query parameters for the NDVI API
      const params = {
        startDate: startDate.value,
        endDate: endDate.value,
        location: location.value,
        temporalResolution: temporalResolution.value,
        aggregation: aggregation.value,
      };

      try {
        const response = await axios.get(apiUrl, { params });
        ndviData.value = response.data; // Store the response in a reactive variable
      } catch (error) {
        console.error("Error fetching NDVI data:", error);
      }
    };

    
     // Calculates yearly averages from time-series data.
    const calculateYearlyAverages = (data) => {
      const yearlyData = {};

      // Group data by year, summing values and counting occurrences
      data.forEach(({ timestamp, value }) => {
        const year = new Date(timestamp * 1000).getFullYear(); // Convert Unix timestamp to year
        if (!yearlyData[year]) yearlyData[year] = { sum: 0, count: 0 };
        yearlyData[year].sum += value;
        yearlyData[year].count += 1;
      });

      // Calculate average for each year and return as an array
      return Object.entries(yearlyData).map(([year, { sum, count }]) => ({
        year: parseInt(year, 10),
        average: sum / count,
      }));
    };

   
    const renderPlot = () => {
      if (temperatureData.value?.data && ndviData.value?.data) {
        // Calculate yearly averages for temperature and NDVI
        const yearlyTemperature = calculateYearlyAverages(
          temperatureData.value.data
        );
        const yearlyNdvi = calculateYearlyAverages(ndviData.value.data);

        // Define trace for temperature data
        const tempTrace = {
          x: yearlyTemperature.map((e) => e.year), 
          y: yearlyTemperature.map((e) => e.average), 
          mode: "lines+markers",
          name: "Temperature (°C)",
          marker: { color: "red", size: 7, symbol: "square" },
          hoverinfo: "text",
          text: yearlyTemperature.map((e) => `${e.average.toFixed(2)}°C`),
        };

        // Define trace for NDVI data
        const ndviTrace = {
          x: yearlyNdvi.map((e) => e.year), 
          y: yearlyNdvi.map((e) => e.average),
          mode: "lines+markers",
          name: "NDVI",
          line: { color: "blue" },
          yaxis: "y2", // Use secondary y-axis for NDVI values
          hoverinfo: "text",
          text: yearlyNdvi.map((e) => `${e.average.toFixed(2)}`),
        };

        // Layout configuration for the dual y-axis plot
        const layout = {
          title: "Yearly NDVI vs. Temperature (2018-2024)",
          xaxis: { title: "Year", type: "category" },
          yaxis: { title: "Temperature (°C)" },
          yaxis2: { title: "NDVI", overlaying: "y", side: "right" },
          template: "plotly_white", 
        };

        // Render the chart using Plotly
        Plotly.newPlot(plotContainer.value, [tempTrace, ndviTrace], layout);
      }
    };

    // Fetch data when the component is mounted
    onMounted(() => {
      fetchTemperatureData();
      fetchNdviData();
    });

    // Watch for updates to temperatureData and ndviData, and render the chart
    watch([temperatureData, ndviData], ([temp, ndvi]) => {
      if (temp && ndvi) renderPlot();
    });

    return { plotContainer }; // Return the reference to the plot container
  },
};
</script>

<style scoped>

.plot-container {
  width: 100%;
  height: 400px;
}
</style>

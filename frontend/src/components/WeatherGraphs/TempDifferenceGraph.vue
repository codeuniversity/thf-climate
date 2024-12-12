<template>
    <div>
      <!-- <h2>{{ graphTitle }}</h2> -->
  
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
      <div ref="plotlyChart" style="width: 100%; height: auto;"></div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, computed } from "vue";
  import axios from "axios";
  import Plotly from "plotly.js-dist-min";
  
  export default {
    name: "TempDifferenceGraph",
    setup() {
      const weatherData = ref(null);
      const startDate = ref("1990-01-01");
      const endDate = ref("2024-11-30");
      const selectedMonth = ref(7); // Default to August (the most severe month) (0-indexed)
      const months = ref([
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ]);
      const plotData = ref([]);
      const plotlyChart = ref(null);
      const historicalMeans = ref([]);
  
      const graphTitle = computed(() => {
        return `Difference from Mean Temperature (1990-2008) in ${
          months.value[selectedMonth.value]
        }`;
      });
  
      // Fetch and calculate historical means for all months (1990-2008)
      const fetchHistoricalMeans = async () => {
        const apiUrl = "https://thf-climate-run-1020174331409.europe-west3.run.app/weather/index";
        const params = {
          weatherVariable: "temperature_2m",
          startDate: new Date("1990-01-01").getTime() / 1000,
          endDate: new Date("2008-12-31").getTime() / 1000,
          location: "TEMPELHOFER_FELD",
          temporalResolution: "MONTHLY",
          aggregation: "MEAN",
        };
  
        try {
          const response = await axios.get(apiUrl, { params });
          const data = response.data?.data;
  
          if (!data || !Array.isArray(data)) {
            console.error("Unexpected data format for historical means:", response);
            return;
          }
  
          // Calculate means for each month (0 = January, 1 = February, etc.)
          const monthlyMeans = Array(12).fill(0).map((_, monthIndex) => {
            const monthData = data.filter((entry) => {
              const date = new Date(entry.timestamp * 1000);
              return date.getMonth() === monthIndex;
            });
  
            const temperatures = monthData.map((entry) => entry.value);
            const total = temperatures.reduce((sum, temp) => sum + temp, 0);
            return temperatures.length > 0 ? total / temperatures.length : null;
          });
  
          historicalMeans.value = monthlyMeans;
        } catch (error) {
          console.error("Error fetching historical means:", error);
        }
      };
  
      // Fetch current weather data
      const fetchData = async () => {
        const apiUrl = "https://thf-climate-run-1020174331409.europe-west3.run.app/weather/index";
        const params = {
          weatherVariable: "temperature_2m",
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
  
      // Process data to compute deviations for the selected month
      const processData = (apiResponse) => {
        if (!apiResponse.data || !Array.isArray(apiResponse.data)) {
          console.log("Unexpected data format:", apiResponse);
          return;
        }
  
        const historicalMean = historicalMeans.value[selectedMonth.value];
        if (historicalMean === null) {
          console.error(`No historical mean available for month: ${selectedMonth.value}`);
          return;
        }
  
        const filteredData = apiResponse.data.filter((entry) => {
          const date = new Date(entry.timestamp * 1000);
          return date.getMonth() === selectedMonth.value;
        });
  
        const years = filteredData.map((entry) =>
          new Date(entry.timestamp * 1000).getFullYear().toString()
        );
        const deviations = filteredData.map(
          (entry) => entry.value - historicalMean
        );
  
        plotData.value = [
          {
            x: years,
            y: deviations,
            type: "bar",
            name: months.value[selectedMonth.value],
            marker: {
              color: deviations.map((dev) =>
                dev >= 0 ? "darkred" : "darkblue"
              ),
            },
            text: deviations.map((dev) => `${dev.toFixed(2)}°C`),
            hoverinfo: "text",
            textposition: "none",
          },
        ];
      };
  
      // Render the Plotly chart
      const renderPlot = () => {
        const layout = {
          title: graphTitle.value,
          xaxis: { title: "Year", type: "category" },
          yaxis: { title: "Deviation from 1990-2008 Mean (°C)" },
          template: "plotly_white",
        };
  
        Plotly.newPlot(plotlyChart.value, plotData.value, layout);
      };
  
      // Fetch all necessary data and render the chart
      const fetchAndRender = async () => {
        await fetchHistoricalMeans(); // Fetch historical means once
        await fetchData(); // Fetch main data
      };
  
      const updateGraph = () => {
        if (startDate.value && endDate.value) {
          fetchData(); // Only fetch main data, since historical means are already cached
        }
      };
  
      onMounted(() => {
        fetchAndRender();
      });
  
      return {
        weatherData,
        startDate,
        endDate,
        selectedMonth,
        months,
        updateGraph,
        plotlyChart,
        graphTitle,
        historicalMeans,
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
  
<template>
<v-container>
  <h2 class="pb-10">Temperature vs. NDVI</h2>
  <v-row justify="center">
    <div
      id="plotlyGraphTemperatureNdvi"
      style="width: 100%; height: 400px"
      class="d-flex justify-center"
    ></div>
  </v-row>
</v-container>
</template>

<script>
import axios from 'axios'
import Plotly from 'plotly.js-dist-min'
import { onMounted, ref, render } from 'vue'

export default {
  name: 'TemperatureNdviBarAndLine',
  setup() {
    const temperatureData = ref(null)
    const ndviData = ref(null)
    const startDate = ref(1514761200) // 2018-01-01
    const endDate = ref(1704063599) // 2023-12-31
    const temporalResolution = ref("Monthly")
    const aggregation = ref("Mean")

    const fetchTemperatureData = async () => {
      const apiUrl = 'http://localhost:8000/weather/index'
      const params = {
        weatherVariable: "temperature_2m",
        startDate: startDate.value,
        endDate: endDate.value,
        location: "TEMPELHOFER_FELD",
        temporalResolution: temporalResolution.value.toUpperCase(),
        aggregation: aggregation.value.toUpperCase()
      }

      try {
        const response = await axios.get(apiUrl, { params })
        temperatureData.value = response.data
        renderPlot()
      } catch (error) {
        console.error("Error fetching temperature data:", error)
      }
    }

    const fetchNdviData = async () => {
      const apiUrl = 'http://localhost:8000/index/ndvi'
      const params = {
        startDate: startDate.value,
        endDate: endDate.value,
        location: "TEMPELHOFER_FELD",
        temporalResolution: temporalResolution.value.toUpperCase(),
        aggregation: aggregation.value.toUpperCase()
      }

      try {
        const response = await axios.get(apiUrl, { params })
        ndviData.value = response.data
        renderPlot()
      } catch (error) {
        console.error("Error fetching NDVI data:", error)
      }
    }

    const renderPlot = () => {
      if (temperatureData.value && ndviData.value) {
        const tempTimestamps = temperatureData.value.data.map(entry =>
          new Date(entry.timestamp * 1000).toISOString().split('T')[0]
        )
        const tempValues = temperatureData.value.data.map(entry => entry.value)
        const ndviTimestamps = ndviData.value.data.map(entry => new Date(entry.timestamp * 1000))
        const ndviValues = ndviData.value.data.map(entry => entry.value)

        const tempTrace = {
          x: tempTimestamps,
          y: tempValues,
          type: 'bar',
          name: 'Temperature (°C)',
          marker: { color: 'red' }
        };

        const ndviTrace = {
          x: ndviTimestamps,
          y: ndviValues,
          mode: 'lines+markers',
          name: 'NDVI',
          line: { color: 'blue' },
          yaxis: 'y2',
        };

        const layout = {
          title: 'NDVI vs. Monthly Temperature for Tempelhofer Feld (2018-2023)',
          xaxis: { title: 'Date', type: 'date', rangeslider: { visible: true } },
          yaxis: { title: 'NDVI' },
          yaxis2: {
            title: 'Temperature (°C)',
            overlaying: 'y',
            side: 'right',
          },
          legend: { x: 1.1, y: 0.5 },
          template: 'plotly_white'
  };

  Plotly.newPlot('plotlyGraphTemperatureNdvi', [tempTrace, ndviTrace], layout);
      }
    }

    onMounted(() => {
      fetchTemperatureData()
      fetchNdviData()
    })
  }
}
</script>

<style scoped></style>

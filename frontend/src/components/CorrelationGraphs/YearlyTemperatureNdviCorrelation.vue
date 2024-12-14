<template>
  <v-container>
    <!-- <h2 class="pb-10">Yearly NDVI vs. Temperature</h2> -->
    <v-row justify="center">
      <div
        ref="plotContainer"
        style="width: 100%; height: 400px"
        class="d-flex justify-center"
      ></div>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios"
import Plotly from "plotly.js-dist-min"
import { onMounted, ref, watch } from "vue"

export default {
  name: "YearlyNdviTemperaturePlot",
  setup() {
    const temperatureData = ref(null)
    const ndviData = ref(null)
    const plotContainer = ref(null)
    const startDate = ref(1514764800) // 2018-01-01
    const endDate = ref(1733007599) // 2024-11-30

    const fetchTemperatureData = async () => {
      const apiUrl =
        "https://thf-climate-run-1020174331409.europe-west3.run.app/weather/index"
      const params = {
        weatherVariable: "temperature_2m",
        startDate: startDate.value,
        endDate: endDate.value,
        location: "TEMPELHOFER_FELD",
        temporalResolution: "MONTHLY",
        aggregation: "MEAN",
      }
      try {
        const response = await axios.get(apiUrl, { params })
        temperatureData.value = response.data
      } catch (error) {
        console.error("Error fetching temperature data:", error)
      }
    }

    const fetchNdviData = async () => {
      const apiUrl =
        "https://thf-climate-run-1020174331409.europe-west3.run.app/index/ndvi"
      const params = {
        startDate: startDate.value,
        endDate: endDate.value,
        location: "TEMPELHOFER_FELD",
        temporalResolution: "MONTHLY",
        aggregation: "MEAN",
      }
      try {
        const response = await axios.get(apiUrl, { params })
        ndviData.value = response.data
      } catch (error) {
        console.error("Error fetching NDVI data:", error)
      }
    }

    const calculateYearlyAverages = (data) => {
      const yearlyData = {}
      data.forEach((entry) => {
        const year = new Date(entry.timestamp * 1000).getFullYear()
        if (!yearlyData[year]) yearlyData[year] = { sum: 0, count: 0 }
        yearlyData[year].sum += entry.value
        yearlyData[year].count += 1
      })
      return Object.entries(yearlyData).map(([year, { sum, count }]) => ({
        year: parseInt(year, 10),
        average: sum / count,
      }))
    }

    const renderPlot = () => {
      if (temperatureData.value && ndviData.value) {
        const yearlyTemperature = calculateYearlyAverages(
          temperatureData.value.data,
        )
        const yearlyNdvi = calculateYearlyAverages(ndviData.value.data)

        const tempTrace = {
          x: yearlyTemperature.map((e) => e.year),
          y: yearlyTemperature.map((e) => e.average),
          mode: "lines+markers",
          name: "Temperature (°C)",
          marker: { color: "red", size: 7, symbol: "square" },
          hoverinfo: "text",
          text: yearlyTemperature.map((e) => `${e.average.toFixed(2)}°C`),
        }

        const ndviTrace = {
          x: yearlyNdvi.map((e) => e.year),
          y: yearlyNdvi.map((e) => e.average),
          mode: "lines+markers",
          name: "NDVI",
          line: { color: "blue" },
          yaxis: "y2",
          hoverinfo: "text",
          text: yearlyNdvi.map((e) => `${e.average.toFixed(2)}`),
        }

        const layout = {
          title: "Yearly NDVI vs. Temperature (2018-2024)",
          xaxis: { title: "Year", type: "category" },
          yaxis: { title: "Temperature (°C)" },
          yaxis2: { title: "NDVI", overlaying: "y", side: "right" },
          template: "plotly_white",
        }

        Plotly.newPlot(plotContainer.value, [tempTrace, ndviTrace], layout)
      }
    }

    onMounted(() => {
      fetchTemperatureData()
      fetchNdviData()
    })

    watch([temperatureData, ndviData], ([temp, ndvi]) => {
      if (temp && ndvi) renderPlot()
    })

    return { plotContainer }
  },
}
</script>

<style scoped></style>

<template>
  <v-container>
    <v-row justify="center" class="pb-16">
      <div
        id="plotlyScatterTemperatureNdvi"
        style="width: 100%; height: 400px"
        class="d-flex justify-center"
      ></div>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios"
import Plotly from "plotly.js-dist-min"
import { onMounted, ref } from "vue"

export default {
  name: "TemperatureNdviScatter",
  setup() {
    const temperatureData = ref(null)
    const ndviData = ref(null)
    const startDate = ref(1514761200) // 2018-01-01
    const endDate = ref(1733007599) // 2024-11-30
    const temporalResolution = ref("Monthly") // options: "Daily", "Monthly"
    const aggregation = ref("Mean") // options: "Mean", "Median", "Max", "Min"

    const fetchTemperatureData = async () => {
      const apiUrl =
        "https://thf-climate-run-1020174331409.europe-west3.run.app/weather/index"
      const params = {
        weatherVariable: "temperature_2m",
        startDate: startDate.value,
        endDate: endDate.value,
        location: "TEMPELHOFER_FELD",
        temporalResolution: temporalResolution.value.toUpperCase(),
        aggregation: aggregation.value.toUpperCase(),
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
      const apiUrl =
        "https://thf-climate-run-1020174331409.europe-west3.run.app/index/ndvi"
      const params = {
        startDate: startDate.value,
        endDate: endDate.value,
        location: "TEMPELHOFER_FELD",
        temporalResolution: temporalResolution.value.toUpperCase(),
        aggregation: aggregation.value.toUpperCase(),
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
        const tempValues = temperatureData.value.data.map(
          (entry) => entry.value,
        )
        const ndviValues = ndviData.value.data.map((entry) => entry.value)

        const timestamps = temperatureData.value.data.map(
          (entry) => entry.timestamp,
        )
        const monthsAndYears = timestamps.map((ts) => {
          const date = new Date(ts * 1000)
          const month = date.toLocaleString("default", { month: "long" })
          const year = date.getFullYear()
          return { month, year }
        })

        // Map months to a circular grayscale gradient
        const months = monthsAndYears.map(({ month }) =>
          new Date(Date.parse(month + " 1")).getMonth(),
        )
        const monthColors = months.map((month) => {
          // Convert month index (0-11) to circular position
          const angle = (month / 12) * 2 * Math.PI // 0-2π range
          // Use cosine to create smooth gradient: July (π) = 0 (black), January (0) = 1 (white)
          const intensity = Math.round(((Math.cos(angle) + 1) / 2) * 255) // Scale cosine to 0-255
          return `rgb(${intensity}, ${intensity}, ${intensity})`
        })

        const scatterTrace = {
          x: tempValues,
          y: ndviValues,
          mode: "markers",
          marker: {
            color: monthColors,
            size: 8,
            line: {
              color: "black",
              width: 1,
            },
          },
          type: "scatter",
          name: "Temperature vs. NDVI",
          hovertemplate:
            "%{x}°C<br>NDVI: %{y}<br>%{customdata.month} %{customdata.year}<extra></extra>",
          customdata: monthsAndYears,
        }

        const layout = {
          title: "Scatter Plot of Temperature vs. NDVI",
          xaxis: { title: "Temperature (°C)" },
          yaxis: { title: "NDVI" },
          template: "plotly_white",
        }

        Plotly.newPlot("plotlyScatterTemperatureNdvi", [scatterTrace], layout)
      }
    }

    onMounted(() => {
      fetchTemperatureData()
      fetchNdviData()
    })
  },
}
</script>

<style scoped></style>

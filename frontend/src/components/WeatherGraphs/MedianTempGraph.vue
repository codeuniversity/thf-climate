<template>
  <div>
    <!-- <h2>Median Monthly Temperature</h2> -->

    <!-- Date Range Input Fields -->
    <!-- <div class="date-picker">
      <label>
        Start Date:
        <input type="date" v-model="startDate" @change="updateDateRange" />
      </label>
      <label>
        End Date:
        <input type="date" v-model="endDate" @change="updateDateRange" />
      </label>
    </div> -->

    <!-- Plotly Chart -->
    <div ref="plotlyChart" style="width: 100%; height: auto"></div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue"
import axios from "axios"
import Plotly from "plotly.js-dist-min"

export default {
  name: "MedianTempGraph",
  setup() {
    const temperatureData = ref(null)
    const startDate = ref("1990-01-01")
    const endDate = ref("2024-11-30")
    const plotData = ref([])
    const plotlyChart = ref(null)

    const fetchTemperatureData = async () => {
      const apiUrl =
        "https://thf-climate-run-1020174331409.europe-west3.run.app/weather/index"

      const params = {
        weatherVariable: "temperature_2m",
        startDate: new Date(startDate.value).getTime() / 1000,
        endDate: new Date(endDate.value).getTime() / 1000,
        location: "TEMPELHOFER_FELD",
        temporalResolution: "MONTHLY",
        aggregation: "MEAN",
      }

      try {
        const response = await axios.get(apiUrl, { params })
        temperatureData.value = response.data
        processData(response.data)
        renderPlot()
      } catch (error) {
        console.error("Error fetching temperature data:", error)
      }
    }

    const processData = (apiResponse) => {
      if (!apiResponse.data || !Array.isArray(apiResponse.data)) {
        console.log("Unexpected data format:", apiResponse)
        return
      }

      const dates = apiResponse.data.map(
        (entry) => new Date(entry.timestamp * 1000).toISOString().split("T")[0],
      )
      const temperatures = apiResponse.data.map((entry) => entry.value)

      plotData.value = [
        {
          x: dates,
          y: temperatures,
          mode: "lines",
          name: "Temperature",
          line: { color: "#FF4136" },
        },
      ]
    }

    const renderPlot = () => {
      const layout = {
        title: "Mean Monthly Temperature (1990 - 2024)",
        xaxis: { title: "", type: "date", rangeslider: { visible: true } },
        yaxis: { title: "Temperature (°C)" },
        template: "plotly_white",
      }

      Plotly.newPlot(plotlyChart.value, plotData.value, layout)
    }

    const updateDateRange = () => {
      if (startDate.value && endDate.value) {
        fetchTemperatureData()
      }
    }

    onMounted(() => {
      fetchTemperatureData()
    })

    return {
      temperatureData,
      startDate,
      endDate,
      updateDateRange,
      plotlyChart,
    }
  },
}
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

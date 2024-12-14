<template>
  <v-container>
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
  name: "YearlyNdviPlot",
  setup() {
    const ndviData = ref(null)
    const plotContainer = ref(null)
    const startDate = ref(1514764800) // 2018-01-01
    const endDate = ref(1733007599) // 2024-11-30

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
      if (ndviData.value) {
        const yearlyNdvi = calculateYearlyAverages(ndviData.value.data)

        const ndviTrace = {
          x: yearlyNdvi.map((e) => e.year),
          y: yearlyNdvi.map((e) => e.average),
          mode: "lines+markers",
          name: "NDVI",
          line: { color: "blue" },
          hoverinfo: "text",
          text: yearlyNdvi.map((e) => `${e.average.toFixed(2)}`),
        }

        const layout = {
          title: "Yearly NDVI (2018-2024)",
          xaxis: { title: "Year", type: "category" },
          yaxis: { title: "NDVI" },
          template: "plotly_white",
        }

        Plotly.newPlot(plotContainer.value, [ndviTrace], layout)
      }
    }

    onMounted(() => {
      fetchNdviData()
    })

    watch(ndviData, (ndvi) => {
      if (ndvi) renderPlot()
    })

    return { plotContainer }
  },
}
</script>

<style scoped></style>

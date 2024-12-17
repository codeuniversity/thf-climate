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
import Plotly from "plotly.js-dist-min"
import { ref, watch } from "vue"

export default {
  name: "YearlyNdviPlot",
  props: {
    ndviData: Object,
    required: true,
  },
  setup(props) {
    const plotContainer = ref(null)

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
      if (props.ndviData) {
        const yearlyNdvi = calculateYearlyAverages(props.ndviData.data)

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

    watch(() => props.ndviData, renderPlot)

    return { plotContainer }
  },
}
</script>

<style scoped></style>

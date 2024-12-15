<template>
  <v-container>
    <v-row>
      <div
        id="plotlyGraphNdviOverlay"
        style="width: 100%; height: 400px"
        class="d-flex justify-center"
      ></div>
    </v-row>
  </v-container>
</template>

<script>
import { watch } from "vue"
import Plotly from "plotly.js-dist-min"

export default {
  name: "NdviComparisonOverlay",
  props: {
    ndviData: Object,
    required: true,
  },
  setup(props) {
    const years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]

    const getFilteredDataByYear = (data, year) => {
      return data.filter(
        (d) => new Date(d.timestamp * 1000).getFullYear() === year
      )
    }

    const getMonthsAndValues = (filteredData) => {
      const months = filteredData.map((d) => new Date(d.timestamp * 1000).getMonth() + 1)
      const values = filteredData.map((d) => d.value)
      return { months, values }
    }

    const renderPlot = () => {
      if (props.ndviData && props.ndviData.data) {
        const traces = years.map((year) => {
          const filteredData = getFilteredDataByYear(props.ndviData.data, year)
          const { months, values } = getMonthsAndValues(filteredData)

          return {
            x: months,
            y: values,
            mode: "lines+markers",
            type: "scatter",
            name: `NDVI ${year}`,
            line: { width: 2 },
          }
        })

        const layout = {
          title: "NDVI - Yearly Overlay (2018-2024)",
          xaxis: {
            title: "",
            tickmode: "array",
            tickvals: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ticktext: [
              "Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ],
          },
          yaxis: { title: "NDVI Value" },
        }

        Plotly.newPlot("plotlyGraphNdviOverlay", traces, layout)
      }
    }


    watch(() => props.ndviData, renderPlot)

    return {
      years,
    }
  },
}
</script>

<style scoped>
h2 {
  text-align: center;
}
</style>

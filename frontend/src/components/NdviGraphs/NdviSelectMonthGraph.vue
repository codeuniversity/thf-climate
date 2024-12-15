<template>
  <v-container>
    <!-- <v-row justify="center">
      <v-col class="py-0" style="max-width: 350px">
        <v-select 
          v-model="month" 
          :items="monthOptions" 
          label="Month" 
          variant="outlined"
          density="compact"
          required 
        />
      </v-col>
    </v-row> -->
    <v-row>
      <div
        id="plotlyGraphNdviMonthly"
        style="width: 100%; height: 400px"
        class="d-flex justify-center"
      ></div>
    </v-row>
  </v-container>
</template>

<script>
import { ref, watch } from "vue"
import Plotly from "plotly.js-dist-min"

export default {
  name: "NdviSelectMonthGraph",
  props: {
    ndviData: Object,
    required: true,
  },
  setup(props) {
    const month = ref("January")
    const monthOptions = [
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
    ]

    const renderPlot = () => {
      if (props.ndviData && props.ndviData.data) {
        const monthIndex = monthOptions.indexOf(month.value) + 1
        const filteredData = props.ndviData.data.filter(
          (d) => new Date(d.timestamp * 1000).getMonth() + 1 === monthIndex,
        )

        const years = filteredData.map((d) =>
          new Date(d.timestamp * 1000).getFullYear(),
        )
        const values = filteredData.map((d) => d.value)

        const trace = {
          x: years,
          y: values,
          mode: "lines+markers",
          type: "bar",
          name: "",
          marker: { color: "green" },
        }

        const layout = {
          title: `NDVI in ${month.value}`,
          xaxis: { title: "" },
          yaxis: { title: "NDVI Value" },
        }

        Plotly.newPlot("plotlyGraphNdviMonthly", [trace], layout)
      }
    }

    watch(month, renderPlot)
    watch(() => props.ndviData, renderPlot)

    return {
      monthOptions,
      month,
    }
  },
}
</script>

<style scoped>
h2 {
  text-align: center;
}
</style>

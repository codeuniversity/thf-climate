<template>
  <v-container>
    <h2 class="pb-10">NDVI Monthly Means (2018-2023)</h2>
    <v-row justify="center">
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
    </v-row>
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
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'
import Plotly from 'plotly.js-dist-min'

export default {
  name: 'NdviSelectMonthGraph',
  setup() {
    const ndviData = ref(null)
    const month = ref("January")
    const monthOptions = [
      "January", "February", "March", "April",
      "May", "June", "July", "August",
      "September", "October", "November", "December"
    ]
    const startDate = ref(1514761200) // 2018-01-01
    const endDate = ref(1704063599) // 2023-12-31

    const fetchNdviData = async () => {
      const apiUrl = 'https://thf-climate-run-1020174331409.europe-west3.run.app/index/ndvi'
      try {
        const response = await axios.get(apiUrl, { 
          params: { 
            startDate: startDate.value,
            endDate: endDate.value,
            location: "TEMPELHOFER_FELD",
            temporalResolution: "MONTHLY",
            aggregation: "MEAN" 
          }
        })
        ndviData.value = response.data
        renderPlot()
      } catch (error) {
        console.error("Error fetching NDVI data:", error)
      }
    }

    const renderPlot = () => {
      if (ndviData.value && ndviData.value.data) {
        const monthIndex = monthOptions.indexOf(month.value) + 1
        const filteredData = ndviData.value.data.filter(d => new Date(d.timestamp * 1000).getMonth() + 1 === monthIndex)
        
        const years = filteredData.map(d => new Date(d.timestamp * 1000).getFullYear())
        const values = filteredData.map(d => d.value)

        const trace = {
          x: years,
          y: values,
          mode: 'lines+markers',
          type: 'bar',
          name: '',
          marker: { color: 'green' }
        }

        const layout = {
          title: `NDVI of Tempelhofer Feld (${month.value})`,
          xaxis: { title: '' },
          yaxis: { title: 'NDVI Value' }
        }

        Plotly.newPlot('plotlyGraphNdviMonthly', [trace], layout)
      }
    }

    watch(month, renderPlot)

    onMounted(() => {
      fetchNdviData()
    })

    return {
      ndviData,
      monthOptions,
      month
    }
  }
}
</script>

<style scoped>
h2 {
  text-align: center;
}
</style>

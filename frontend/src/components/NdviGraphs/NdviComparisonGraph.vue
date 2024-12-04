<template>
  <v-container>
    <h2 class="pb-10">NDVI (2018-2023)</h2>
    <v-row justify="center">
      <v-col class="py-0" style="max-width: 350px">
        <v-select 
          v-model="temporalResolution" 
          :items="temporalResolutionOptions" 
          label="Temporal Resolution" 
          variant="outlined"
          density="compact"
          required 
        />
      </v-col>
      <v-col 
        v-if="temporalResolution !== 'Daily'" 
        class="py-0" 
        style="max-width: 350px"
      >
        <v-select 
          v-model="aggregation" 
          :items="aggregationOptions" 
          label="Aggregation"
          variant="outlined"
          density="compact"
          required 
        />
      </v-col>
    </v-row>
    <v-row>
      <div 
        id="plotlyGraphNdviComparison" 
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
  name: 'NdviComparisonGraph',
  setup() {
    const ndviData = ref(null)
    const startDate = ref(1514761200) // 2018-01-01
    const endDate = ref(1704063599) // 2023-12-31
    const temporalResolution = ref("Monthly")
    const aggregation = ref("Mean")
    const temporalResolutionOptions = ["Monthly", "Daily"]
    const aggregationOptions = ["Mean", "Median", "Max", "Min"]

    const fetchNdviData = async (params) => {
      const apiUrl = 'https://thf-climate-run-1020174331409.europe-west3.run.app/index/ndvi'
      try {
        const response = await axios.get(apiUrl, { params })
        ndviData.value = response.data
        renderPlot()
      } catch (error) {
        console.error("Error fetching NDVI data:", error)
      }
    }

    const renderPlot = () => {
      if (ndviData.value && ndviData.value.data) {
        const timestamps = ndviData.value.data.map(d => new Date(d.timestamp * 1000))
        const values = ndviData.value.data.map(d => d.value)
        const trace = {
          x: timestamps,
          y: values,
          mode: 'lines+markers',
          type: 'scatter',
          name: '',
          line: { color: 'blue' }
        }
        const layout = {
          title: 'NDVI of Tempelhofer Feld',
          xaxis: { title: '', type: 'date', rangeslider: { visible: true } },
          yaxis: { title: 'NDVI Value' },
        }
        Plotly.newPlot('plotlyGraphNdviComparison', [trace], layout)
      }
    }

    const updateGraph = () => {
      const params = {
        startDate: startDate.value,
        endDate: endDate.value,
        location: "TEMPELHOFER_FELD",
        temporalResolution: temporalResolution.value.toUpperCase(),
        aggregation: aggregation.value.toUpperCase(),
      }
      fetchNdviData(params)
    }

    watch([temporalResolution, aggregation], updateGraph)

    onMounted(() => {
      const defaultParams = {
        startDate: startDate.value,
        endDate: endDate.value,
        location: "TEMPELHOFER_FELD",
        temporalResolution: temporalResolution.value.toUpperCase(),
        aggregation: aggregation.value.toUpperCase(),
      }
      fetchNdviData(defaultParams)
    })

    return {
      ndviData,
      startDate,
      endDate,
      temporalResolution,
      aggregation,
      temporalResolutionOptions,
      aggregationOptions
    }
  }
}
</script>

<style scoped>
h2 {
  text-align: center;
}
</style>

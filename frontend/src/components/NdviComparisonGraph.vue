<template>
  <v-container>

    <h2 class="mb-0">NDVI of Tempelhofer Feld</h2>
    <v-row class="pb-4">
      <div 
        id="plotlyGraph" 
        v-show="!loading && ndviData"
        style="width: 100%"
        class="d-flex justify-center"
      ></div>
    </v-row>
    <!-- <v-progress-circular 
      v-if="loading" 
      indeterminate 
      class="d-flex mx-auto py-10"
    ></v-progress-circular> -->

    <v-form @submit.prevent="handleSubmit" class="pb-6">
      <v-row>
        <v-col>
          <v-text-field 
            v-model="startDate" 
            label="Start Date" 
            type="number" 
            required 
          />
        </v-col>
        <v-col>
          <v-text-field 
            v-model="endDate" 
            label="End Date" 
            type="number" 
            required 
          />
        </v-col>
        <v-col>
          <v-select 
            v-model="temporalResolution" 
            :items="temporalResolutionOptions" 
            label="Temporal Resolution" 
            required 
          />
        </v-col>
        <v-col>
          <v-select 
            v-model="aggregation" 
            :items="aggregationOptions" 
            label="Aggregation" 
            required 
          />
        </v-col>
      </v-row>
      <v-btn type="submit" color="blue">Update</v-btn>
    </v-form>

  </v-container>
</template>

<script>
import { ref, nextTick, onMounted } from 'vue'
import axios from 'axios'
import Plotly from 'plotly.js-dist-min'

export default {
  name: 'NdviComparisonGraph',
  setup() {
    const ndviData = ref(null)
    const startDate = ref(1514761200)
    const endDate = ref(1704063599)
    const temporalResolution = ref("MONTHLY")
    const aggregation = ref("MEAN")
    const temporalResolutionOptions = ["MONTHLY", "DAILY"]
    const aggregationOptions = ["MEAN", "MEDIAN", "MAX", "MIN"]
    const loading = ref(false)

    const fetchNdviData = async (params, ) => {
      const apiUrl = 'http://localhost:8000/index/ndvi'
      try {
        loading.value = true
        const response = await axios.get(apiUrl, { params: params })
        ndviData.value = response.data
        // Wait for DOM to update before rendering Plotly graph
        await nextTick()
        renderPlot()
      } catch (error) {
        console.error("Error fetching NDVI data:", error)
      } finally {
        loading.value = false
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
          name: 'NDVI',
          line: {
            color: 'blue',
            width: 2,
            dash: 'solid',
          },
          marker: {
            color: 'red',
            size: 6,
          }
        }
        const layout = {
          title: 'NDVI of Tempelhofer Feld (2018 - 2023)',
          xaxis: { title: 'Date' },
          yaxis: { title: 'NDVI Value' },
        }
        Plotly.newPlot('plotlyGraph', [trace], layout)
      }
    }

    // Handle form submission
    const handleSubmit = () => {
      const params = {
        startDate: startDate.value,
        endDate: endDate.value,
        location: "TEMPELHOFER_FELD",
        temporalResolution: temporalResolution.value,
        aggregation: aggregation.value,
      }
      fetchNdviData(params)
    }

    onMounted(() => {
      const defaultParams = {
        startDate: startDate.value,
        endDate: endDate.value,
        location: "TEMPELHOFER_FELD",
        temporalResolution: temporalResolution.value,
        aggregation: aggregation.value,
      }
      fetchNdviData(defaultParams)
    })

    return {
      ndviData,
      startDate,
      endDate,
      temporalResolution,
      aggregation,
      loading,
      temporalResolutionOptions,
      aggregationOptions,
      handleSubmit,
    }
  }
}
</script>

<style scoped>
h2 {
  text-align: center;
  margin-bottom: 10px;
}
</style>

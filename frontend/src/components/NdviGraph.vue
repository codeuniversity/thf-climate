<template>
  <v-container>
    <h3 class="pb-6">NDVI Comparison</h3>
    <v-form @submit.prevent="handleSubmit" class="pb-4">
      <h6>Graph 1</h6>
      <v-row>
        <!-- Graph 1 -->
        <v-col>
          <v-text-field 
            v-model="startDate1" 
            label="Start Date" 
            type="number" 
            required 
          />
        </v-col>
        <v-col>
          <v-text-field 
            v-model="endDate1" 
            label="End Date" 
            type="number" 
            required 
          />
        </v-col>
        <v-col>
          <v-select 
            v-model="temporalResolution1" 
            :items="temporalResolutionOptions" 
            label="Temporal Resolution" 
            required 
          />
        </v-col>
        <v-col>
          <v-select 
            v-model="aggregation1" 
            :items="aggregationOptions" 
            label="Aggregation" 
            required 
          />
        </v-col>
      </v-row>
        <!-- Graph 2 -->
      <h6>Graph 2</h6>
      <v-row>
        <v-col>
          <v-text-field 
            v-model="startDate2" 
            label="Start Date" 
            type="number" 
            required 
          />
        </v-col>
        <v-col>
          <v-text-field 
            v-model="endDate2" 
            label="End Date" 
            type="number" 
            required 
          />
        </v-col>
        <v-col>
          <v-select 
            v-model="temporalResolution2" 
            :items="temporalResolutionOptions" 
            label="Temporal Resolution" 
            required 
          />
        </v-col>
        <v-col>
          <v-select 
            v-model="aggregation2" 
            :items="aggregationOptions" 
            label="Aggregation" 
            required 
          />
        </v-col>
      </v-row>
      <v-btn type="submit" color="blue">Submit</v-btn>
    </v-form>
    <v-progress-circular 
      v-if="loading" 
      indeterminate 
      class="d-flex mx-auto mb-4"
    ></v-progress-circular>
    <v-row>
      <div id="plotlyGraph1" v-show="!loading && ndviData1" style="width: 550px;"></div>
      <div id="plotlyGraph2" v-show="!loading && ndviData2" style="width: 550px;"></div>
    </v-row>
    
  </v-container>
</template>
<script>
import { ref, nextTick } from 'vue'
import axios from 'axios'
import Plotly from 'plotly.js-dist-min'
export default {
  name: 'NdviGraphComparison',
  setup() {
    const ndviData1 = ref(null)
    const startDate1 = ref(1514761200)
    const endDate1 = ref(1546297199)
    const temporalResolution1 = ref("MONTHLY")
    const aggregation1 = ref("MEAN")
  
    const ndviData2 = ref(null)
    const startDate2 = ref(1672527600)
    const endDate2 = ref(1704063599)
    const temporalResolution2 = ref("MONTHLY")
    const aggregation2 = ref("MEAN")
    const temporalResolutionOptions = ["MONTHLY", "DAILY"]
    const aggregationOptions = ["MEAN", "MEDIAN", "MAX", "MIN"]
    const loading = ref(false)
    const fetchNdviData = async (params1, params2) => {
      const apiUrl = 'http://localhost:8000/index/ndvi'
      try {
        loading.value = true
        const response1 = await axios.get(apiUrl, { params: params1 })
        ndviData1.value = response1.data
        const response2 = await axios.get(apiUrl, { params: params2 })
        ndviData2.value = response2.data
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
      if (ndviData1.value && ndviData1.value.data) {
        const timestamps1 = ndviData1.value.data.map(d => new Date(d.timestamp * 1000))
        const values1 = ndviData1.value.data.map(d => d.value)
        const trace1 = {
          x: timestamps1,
          y: values1,
          mode: 'lines+markers',
          type: 'scatter',
          name: 'NDVI - Graph 1',
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
        const layout1 = {
          title: 'NDVI Graph 1',
          xaxis: { title: 'Date' },
          yaxis: { title: 'NDVI Value' },
        }
        Plotly.newPlot('plotlyGraph1', [trace1], layout1)
      }
      if (ndviData2.value && ndviData2.value.data) {
        const timestamps2 = ndviData2.value.data.map(d => new Date(d.timestamp * 1000))
        const values2 = ndviData2.value.data.map(d => d.value)
        const trace2 = {
          x: timestamps2,
          y: values2,
          mode: 'lines+markers',
          type: 'scatter',
          name: 'NDVI - Graph 2',
          line: {
            color: 'green',
            width: 2,
            dash: 'solid',
          },
          marker: {
            color: 'orange',
            size: 6,
          }
        }
        const layout2 = {
          title: 'NDVI Graph 2',
          xaxis: { title: 'Date' },
          yaxis: { title: 'NDVI Value' },
        }
        Plotly.newPlot('plotlyGraph2', [trace2], layout2)
      }
    }
    // Handle form submission
    const handleSubmit = () => {
      const params1 = {
        startDate: startDate1.value,
        endDate: endDate1.value,
        location: "TEMPELHOFER_FELD",
        temporalResolution: temporalResolution1.value,
        aggregation: aggregation1.value,
      }
      const params2 = {
        startDate: startDate2.value,
        endDate: endDate2.value,
        location: "TEMPELHOFER_FELD",
        temporalResolution: temporalResolution2.value,
        aggregation: aggregation2.value,
      }
      fetchNdviData(params1, params2)
    }
    return {
      ndviData1,
      ndviData2,
      startDate1,
      endDate1,
      temporalResolution1,
      aggregation1,
      startDate2,
      endDate2,
      temporalResolution2,
      aggregation2,
      loading,
      temporalResolutionOptions,
      aggregationOptions,
      handleSubmit,
    }
  }
}
</script>

<style scoped></style>

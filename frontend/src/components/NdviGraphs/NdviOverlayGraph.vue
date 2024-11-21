<template>
    <v-container>
      <h2 class="pb-10">NDVI Year Overlay (2018-2023)</h2>
      <v-row>
        <div 
          id="plotlyGraphNdviOverlay" 
          v-show="ndviData"
          style="width: 100%"
          class="d-flex justify-center"
        ></div>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import { ref, nextTick, onMounted } from 'vue'
  import axios from 'axios'
  import Plotly from 'plotly.js-dist-min'
  
  export default {
    name: 'NdviComparisonOverlay',
    setup() {
      const ndviData = ref(null)
      const startDate = ref(1514761200) // 2018-01-01
      const endDate = ref(1704063599) // 2023-12-31
      const years = [2018, 2019, 2020, 2021, 2022, 2023]
  
      const fetchNdviData = async (params) => {
        const apiUrl = 'http://localhost:8000/index/ndvi'
        try {
          const response = await axios.get(apiUrl, { params })
          ndviData.value = response.data
          await nextTick()
          renderPlot()
        } catch (error) {
          console.error("Error fetching NDVI data:", error)
        }
      }
  
      const renderPlot = () => {
        if (ndviData.value && ndviData.value.data) {
          const traces = years.map(year => {
            const filteredData = ndviData.value.data.filter(d => new Date(d.timestamp * 1000).getFullYear() === year)
  
            const months = filteredData.map(d => new Date(d.timestamp * 1000).getMonth() + 1)
            const values = filteredData.map(d => d.value)
  
            return {
              x: months,
              y: values,
              mode: 'lines+markers',
              type: 'scatter',
              name: `NDVI ${year}`,
              line: { width: 2 },
            }
          })
  
          const layout = {
            title: 'NDVI of Tempelhofer Feld',
            xaxis: { 
              title: '', 
              tickmode: 'array', 
              tickvals: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
              ticktext: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            },
            yaxis: { title: 'NDVI Value' },
          }
  
          Plotly.newPlot('plotlyGraphNdviOverlay', traces, layout)
        }
      }
  
      onMounted(() => {
        const params = {
          startDate: startDate.value,
          endDate: endDate.value,
          location: "TEMPELHOFER_FELD",
          temporalResolution: "MONTHLY",
          aggregation: "MEAN",
        }
        fetchNdviData(params)
      })
  
      return {
        ndviData,
        years,
      }
    }
  }
  </script>
  
  <style scoped>
  h2 {
    text-align: center;
  }
  </style>
  
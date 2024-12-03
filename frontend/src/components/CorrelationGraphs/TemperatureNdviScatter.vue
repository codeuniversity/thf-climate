<template>
    <v-container>
      <v-row justify="center" class="pb-16">
        <div
          id="plotlyScatterTemperatureNdvi"
          style="width: 100%; height: 400px"
          class="d-flex justify-center"
        ></div>
      </v-row>
    </v-container>
    </template>
    
    <script>
    import axios from 'axios'
    import Plotly from 'plotly.js-dist-min'
    import { onMounted, ref, render } from 'vue'
    
    export default {
      name: 'TemperatureNdviScatter',
      setup() {
        const temperatureData = ref(null)
        const ndviData = ref(null)
        const startDate = ref(1514761200) // 2018-01-01
        const endDate = ref(1704063599) // 2023-12-31
        const temporalResolution = ref("Monthly") // options: "Daily", "Monthly"
        const aggregation = ref("Mean") // options: "Mean", "Median", "Max", "Min"
    
        const fetchTemperatureData = async () => {
          const apiUrl = 'https://thf-climate-run-1020174331409.europe-west3.run.app/weather/index'
          const params = {
            weatherVariable: "temperature_2m",
            startDate: startDate.value,
            endDate: endDate.value,
            location: "TEMPELHOFER_FELD",
            temporalResolution: temporalResolution.value.toUpperCase(),
            aggregation: aggregation.value.toUpperCase()
          }
    
          try {
            const response = await axios.get(apiUrl, { params })
            temperatureData.value = response.data
            renderPlot()
          } catch (error) {
            console.error("Error fetching temperature data:", error)
          }
        }
    
        const fetchNdviData = async () => {
          const apiUrl = 'https://thf-climate-run-1020174331409.europe-west3.run.app/index/ndvi'
          const params = {
            startDate: startDate.value,
            endDate: endDate.value,
            location: "TEMPELHOFER_FELD",
            temporalResolution: temporalResolution.value.toUpperCase(),
            aggregation: aggregation.value.toUpperCase()
          }
    
          try {
            const response = await axios.get(apiUrl, { params })
            ndviData.value = response.data
            renderPlot()
          } catch (error) {
            console.error("Error fetching NDVI data:", error)
          }
        }

        const calculateRegression = (xValues, yValues) => {
          const n = xValues.length
          const sumX = xValues.reduce((acc, val) => acc + val, 0)
          const sumY = yValues.reduce((acc, val) => acc + val, 0)
          const sumXY = xValues.reduce((acc, val, index) => acc + val * yValues[index], 0)
          const sumX2 = xValues.reduce((acc, val) => acc + val * val, 0)

          const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX)
          const intercept = (sumY - slope * sumX) / n

          return { slope, intercept }
        }
    
        const renderPlot = () => {
          if (temperatureData.value && ndviData.value) {
            const tempValues = temperatureData.value.data.map(entry => entry.value)
            const ndviValues = ndviData.value.data.map(entry => entry.value)

            const { slope, intercept } = calculateRegression(tempValues, ndviValues)
            const trendLineValues = tempValues.map(x => slope * x + intercept)
            const trendlineEquation = `y = ${slope.toFixed(2)}x + ${intercept.toFixed(2)}`;

            const scatterTrace = {
              x: tempValues,
              y: ndviValues,
              mode: 'markers',
              marker: { color: 'green' },
              type: 'scatter',
              name: 'Temperature vs NDVI'
            }

            const trendLineTrace = {
              x: tempValues,
              y: trendLineValues,
              mode: 'lines',
              line: { color: 'grey', dash: 'dash' },
              type: 'scatter',
              name: `Trend Line: ${trendlineEquation}`
            }

            const layout = {
              title: 'Scatter Plot of Temperature vs. NDVI',
              xaxis: { title: 'Temperature (°C)' },
              yaxis: { title: 'NDVI' },
              template: 'plotly_white',
              legend: { x: 1.02, y: 0.5 },
            }

            Plotly.newPlot('plotlyScatterTemperatureNdvi', [scatterTrace, trendLineTrace], layout)
          }
        }
    
        onMounted(() => {
          fetchTemperatureData()
          fetchNdviData()
        })
      }
    }
    </script>
    
    <style scoped></style>
    
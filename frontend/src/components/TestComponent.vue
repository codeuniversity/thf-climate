// src/components/FetchTemperatureData.vue
<template>
  <div>
    <h3>Temperature Data:</h3>
    <ul v-if="temperatureData">
      <li v-for="(data, index) in temperatureData.data" :key="index">
        Timestamp: {{ data.timestamp }} - Value: {{ data.value }} °C
      </li>
    </ul>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'FetchTemperatureData',
  setup() {
    const temperatureData = ref(null)

    const fetchTemperatureData = async () => {
      const apiUrl = 'http://localhost:8000/weather/temp'
      
      const params = {
        startDate: 1672527600,
        endDate: 1675119600,
        location: "TEMPELHOFER-FELD",
        temporalResolution: "DAILY",
        aggregation: "MEAN",
      }

      try {
        const response = await axios.get(apiUrl, { params })
        temperatureData.value = response.data
      } catch (error) {
        console.error("Error fetching temperature data:", error)
      }
    }

    onMounted(() => {
      fetchTemperatureData()
    })

    return {
      temperatureData
    }
  }
}
</script>

<style scoped></style>

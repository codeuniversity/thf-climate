<template>
  <v-container class="main-section" fluid>
    <!-- <Images />
    <NdviComparisonGraph />
    <NdviSelectMonthGraph />
    <NdviOverlayGraph />
    <MedianTempGraph />
    <MeanSoilTempGraph />
    <MeanSoilMoistureGraph />
    <AugustMeanSoilTempGraph />
    <SelectMonthMeanSoilTempGraph /> -->
    <TemperatureNdviBarAndLine />
  </v-container>
</template>

<script>
import Images from "./Images.vue"
import NdviComparisonGraph from "./NdviGraphs/NdviComparisonGraph.vue"
import NdviSelectMonthGraph from "./NdviGraphs/NdviSelectMonthGraph.vue"
import NdviOverlayGraph from "./NdviGraphs/NdviOverlayGraph.vue"
import MedianTempGraph from "./WeatherGraphs/MedianTempGraph.vue"
import MeanSoilTempGraph from "./WeatherGraphs/SoilTempGraph.vue"
import MeanSoilMoistureGraph from "./WeatherGraphs/SoilMoistureGraph.vue"
import AugustMeanSoilTempGraph from "./WeatherGraphs/AugustSoilTempGraph.vue"
import SelectMonthMeanSoilTempGraph from "./WeatherGraphs/SelectMonthSoilTempGraph.vue"
import TemperatureNdviGraph from "./CorrelationGraphs/TemperatureNdviBarAndLine.vue"
import TemperatureNdviBarAndLine from "./CorrelationGraphs/TemperatureNdviBarAndLine.vue"

export default {
  name: 'MainSection',
  components: {
    Images,
    NdviComparisonGraph,
    NdviSelectMonthGraph,
    NdviOverlayGraph,
    MedianTempGraph,
    MeanSoilTempGraph,
    MeanSoilMoistureGraph,
    AugustMeanSoilTempGraph,
    SelectMonthMeanSoilTempGraph,
    TemperatureNdviBarAndLine
  }
}
</script>

<style scoped>
.main-section {
  margin: 50px 0;
  text-align: center;
}

.main-text {
  font-size: 1.2rem;
  font-weight: 300;
}
</style>

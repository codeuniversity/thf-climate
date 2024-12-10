<template>
  <v-container class="main-section" fluid>
    <Ndvi />
    <Images />
    <NdviSelectMonthGraph />
    <NdviOverlayGraph />
    <TempVsNdvi />
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
import TemperatureNdviBarAndLine from "./CorrelationGraphs/TemperatureNdviBarAndLine.vue"
import TemperatureNdviScatter from "./CorrelationGraphs/TemperatureNdviScatter.vue"
import TempDifferenceGraph from "./WeatherGraphs/TempDifferenceGraph.vue"
import SoilTempDifferenceGraph from "./WeatherGraphs/SoilTempDifferenceGraph.vue"
import NdviDifferenceGraph from "./NdviGraphs/NdviDifferenceGraph.vue"
import Ndvi from "./Text/Ndvi.vue"
import TempVsNdvi from "./Text/TempVsNdvi.vue"

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
    TempDifferenceGraph,
    SoilTempDifferenceGraph,
    TemperatureNdviBarAndLine,
    TemperatureNdviScatter,
    NdviDifferenceGraph,
    Ndvi,
    TempVsNdvi
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

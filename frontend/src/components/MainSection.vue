<template>
  <v-container class="main-section" fluid>
    <YearlyNdviTemperaturePlot />
    <TemperatureNdviBarAndLine />
    <TemperatureNdviScatter />
    <TempDifferenceGraph />
    <SoilTempDifferenceGraph />
    <NdviDifferenceGraph />
    <NdviOverlayGraph />
    <!-- <Images />
    <NdviComparisonGraph />
    <NdviSelectMonthGraph />
    <MedianTempGraph />
    <MeanSoilTempGraph />
    <MeanSoilMoistureGraph />
    <AugustMeanSoilTempGraph />
    <SelectMonthMeanSoilTempGraph /> -->
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
import YearlyNdviTemperaturePlot from "./CorrelationGraphs/YearlyTemperatureNdviCorrelation.vue"

export default {
  name: 'MainSection',
  components: {
    Images,
    YearlyNdviTemperaturePlot,
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
    NdviDifferenceGraph
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

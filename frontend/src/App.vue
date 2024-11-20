<template>
  <h1 id="app">
    <NdviComparisonGraph />
    <MedianTempGraph />
    <MeanSoilTempGraph />
    <MeanSoilMoistureGraph />
    <AugustMeanSoilTempGraph />
    <SelectMonthMeanSoilTempGraph />
  </h1>
</template>

<script>
  import NdviComparisonGraph from "./components/NdviComparisonGraph.vue"
  import MedianTempGraph from "./components/MedianTempGraph.vue"
  import MeanSoilTempGraph from "./components/SoilTempGraph.vue"
  import MeanSoilMoistureGraph from "./components/SoilMoistureGraph.vue"
  import AugustMeanSoilTempGraph from "./components/AugustSoilTempGraph.vue"
  import SelectMonthMeanSoilTempGraph from "./components/SelectMonthSoilTempGraph.vue"

  export default {
    name: 'App',
    components: {
      NdviComparisonGraph,
      MedianTempGraph,
      MeanSoilTempGraph,
      MeanSoilMoistureGraph,
      AugustMeanSoilTempGraph,
      SelectMonthMeanSoilTempGraph
    }
  }
</script>

<style scoped></style>

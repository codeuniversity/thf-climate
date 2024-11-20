<template>
  <h1 id="app">
    <NdviGraph />
    <MedianTempGraph />
    <MeanSoilTempGraph />
    <MeanSoilMoistureGraph />
    <AugustMeanSoilTempGraph />
    <SelectMonthMeanSoilTempGraph />
  </h1>
</template>

<script>
  import NdviGraph from "./components/NdviGraph.vue"
  import MedianTempGraph from "./components/TestGraphOne.vue"
  import MeanSoilTempGraph from "./components/SoilTempGraph.vue"
  import MeanSoilMoistureGraph from "./components/SoilMoistureGraph.vue"
  import AugustMeanSoilTempGraph from "./components/AugustSoilTempGraph.vue"
  import SelectMonthMeanSoilTempGraph from "./components/SelectMonthSoilTempGraph.vue"

  export default {
    name: 'App',
    components: {
      NdviGraph,
      MedianTempGraph,
      MeanSoilTempGraph,
      MeanSoilMoistureGraph,
      AugustMeanSoilTempGraph,
      SelectMonthMeanSoilTempGraph
    }
  }
</script>

<style scoped></style>

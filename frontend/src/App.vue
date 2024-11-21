<template>
  <h1 id="app">
    <TestComponent />
    <MedianTempGraph />
    <MeanSoilTempGraph />
    <MeanSoilMoistureGraph />
    <AugustMeanSoilTempGraph />
    <SelectMonthMeanSoilTempGraph />
  </h1>
</template>

<script>
  import TestComponent from "./components/TestComponent.vue"
  import MedianTempGraph from "./components/TestGraphOne.vue"
  import MeanSoilTempGraph from "./components/SoilTempGraph.vue"
  import MeanSoilMoistureGraph from "./components/SoilMoistureGraph.vue"
  import AugustMeanSoilTempGraph from "./components/AugustSoilTempGraph.vue"
  import SelectMonthMeanSoilTempGraph from "./components/SelectMonthSoilTempGraph.vue"

  export default {
    name: 'App',
    components: {
      //TestComponent,
      MedianTempGraph,
      MeanSoilTempGraph,
      MeanSoilMoistureGraph,
      AugustMeanSoilTempGraph,
      SelectMonthMeanSoilTempGraph
    }
  };
</script>

<style scoped></style>

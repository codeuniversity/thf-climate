<template>
  <h1 id="app">
    <NdviGraph />
  </h1>
</template>

<script>
  import NdviGraph from "./components/NdviGraph.vue"
  import MedianTempGraph from "./components/TestGraphOne.vue"

  export default {
    name: 'App',
    components: {
      NdviGraph,
      MedianTempGraph
    }
  }
</script>

<style scoped></style>

<template>
  <h1 id="app">
    <TestComponent />
    <MedianTempGraph />
  </h1>
</template>

<script>
  import TestComponent from "./components/TestComponent.vue"
  import MedianTempGraph from "./components/TestGraphOne.vue"

  export default {
    name: 'App',
    components: {
      TestComponent,
      MedianTempGraph
    }
  };
</script>

<style scoped></style>

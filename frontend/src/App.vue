<template>
  <h1 id="app">
    <TestComponent />
  </h1>
</template>

<script>
  import TestComponent from "./components/TestComponent.vue"

  export default {
    name: 'App',
    components: {
      TestComponent
    }
  };
</script>

<style scoped></style>

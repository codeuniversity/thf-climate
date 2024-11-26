<template>
  <h1 id="app">
    <Header />
    <IntroSection />
    <MainSection />
    <!-- <MedianTempGraph />
    <MeanSoilTempGraph />
    <MeanSoilMoistureGraph />
    <AugustMeanSoilTempGraph />
    <SelectMonthMeanSoilTempGraph /> -->
    <Footer />
  </h1>
</template>

<script>
  import Header from "./components/Header.vue"
  import IntroSection from "./components/IntroSection.vue"
  import MainSection from "./components/MainSection.vue"
  import MedianTempGraph from "./components/TestGraphOne.vue"
  import MeanSoilTempGraph from "./components/SoilTempGraph.vue"
  import MeanSoilMoistureGraph from "./components/SoilMoistureGraph.vue"
  import AugustMeanSoilTempGraph from "./components/AugustSoilTempGraph.vue"
  import SelectMonthMeanSoilTempGraph from "./components/SelectMonthSoilTempGraph.vue"
  import Footer from "./components/Footer.vue"

  export default {
    name: 'App',
    components: {
      Header,
      IntroSection,
      MainSection,
      MedianTempGraph,
      MeanSoilTempGraph,
      MeanSoilMoistureGraph,
      AugustMeanSoilTempGraph,
      SelectMonthMeanSoilTempGraph,
      Footer
    }
  };
</script>

<style scoped></style>

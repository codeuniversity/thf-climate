<template>
  <h1 id="app">
    <Header />
    <IntroSection />
    <MainSection />
    <Footer />
  </h1>
</template>

<script>
  import Header from "./components/Header.vue"
  import IntroSection from "./components/IntroSection.vue"
  import MainSection from "./components/MainSection.vue"
  import Footer from "./components/Footer.vue"

  export default {
    name: 'App',
    components: {
      Header,
      IntroSection,
      MainSection,
      Footer
    }
  }
</script>

<style scoped></style>

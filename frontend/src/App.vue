<template>
  <div id="app">
    <Header />
    <IntroSection />
    <MainSection />
    <AboutSection />
    <Footer />
  </div>
</template>

<script>
import Header from "./components/Header.vue"
import IntroSection from "./components/IntroSection.vue"
import MainSection from "./components/MainSection.vue"
import Footer from "./components/Footer.vue"
import AboutSection from "./components/AboutSection.vue"

export default {
  name: "App",
  components: {
    Header,
    IntroSection,
    MainSection,
    Footer,
    AboutSection,
  },
}
</script>

<style scoped></style>

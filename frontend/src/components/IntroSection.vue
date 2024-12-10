<template>
  <v-container class="introduction-section" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <p style="font-weight: 600; font-size: 1.4rem">
          The climate is changing, and so is the vegetation at Berlin’s beloved Tempelhofer Feld.
        </p>
        <p class="intro-text pt-10">
          Welcome to our interactive exploration of Tempelhofer Feld, a unique urban oasis in Berlin. Once an airport in the middle of the city, this vast field has transformed into a public park, offering a fascinating case study of how urban green spaces evolve and respond to changes in climate. 
        </p>
        <p class="intro-text pt-6">
          While most studies relating to the vegetation and effects of climate change on Tempelhofer Feld have been carried out on the ground, we have decided to look at the park from high above, using Sentinel-2 satellite imagery from 2018-2024 and the satellite-derived measurement NDVI (normalized difference vegetation index) powered by Google Earth Engine.
        </p>
        <p class="intro-text pt-6">
          Harnessing earth observation methods in the research of climate change and its effects opens new and exciting opportunities, not to mention the labor saved by using freely accessible data. In this study, for example, variations in NDVI can be analyzed in relation to the changing climate by looking at trends in NDVI over the course of several years and in relation to temperature and other weather measurements.
        </p>
        <p class="intro-text pt-6">
          We found that [main results here]. 
        </p>
        <p class="intro-text pt-12">
          Visual here
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'IntroSection',
  data() {
    return {
      //
    }
  }
}
</script>

<style scoped>
.introduction-section {
  margin: 50px 0;
  text-align: center;
}

.intro-text {
  font-size: 1.2rem;
  font-weight: 300;
}
</style>

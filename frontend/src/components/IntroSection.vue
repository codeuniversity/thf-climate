<template>
  <v-container class="introduction-section pb-16" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10" class="pt-10">
        <p style="font-weight: 600; font-size: 1.4rem">
          The climate is changing, and so is the vegetation at Berlin’s beloved Tempelhofer Feld.
        </p>
        <p class="intro-text pt-10">
          Climate Change is affecting the whole globe, but changes are also visible in small local scope. “Tempelhofer Feld” is a unique urban oasis in Berlin. Once an airport in the middle of the city, this vast field has transformed into a public park, offering a fascinating case study of how urban green spaces evolve and respond to changes in climate. 
        </p>
        <p class="intro-text pt-6">
          We analyzed the micro-climate of this unique area by deriving vegetation indices from high-resolution satellite imagery and utilizing long-term in-vitro sensors. Check out the results yourself.
        </p>
        <p class="pt-10">
          Quick Navigation: 
          +++ Temperature 
          +++ What is NDVI 
          +++ NDVI 
          +++ Correlations 
          +++ Interpretation 
          +++ Team and Project
        </p>
        <img 
          src="@/assets/images/snow-thf-dec-2010.png" 
          alt="Several centimeters of snow and people cross country skiing on Tempelhofer Feld" 
          class="pt-10"
        />
        <br />
        <img 
          src="@/assets/images/no-snow-thf-dec-2024.png" 
          alt="People enjoying Tempelhofer Feld"
          class="pt-10"
        />
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
  text-align: center;
}

.intro-text {
  font-size: 1.2rem;
  font-weight: 300;
}
</style>

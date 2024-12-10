<template>
    <v-container class="temp-ndvi-text-section" fluid>
      <v-row justify="center">
        <v-col cols="12" md="10">
          <p style="font-weight: 600; font-size: 1.4rem">
            Temperature vs. NDVI
          </p>
          <p class="temp-ndvi-text pt-10">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eget odio luctus, facilisis ipsum sit amet, tristique nulla. Integer porttitor porta facilisis. Sed quam nisi, tincidunt ut nisi ac, faucibus facilisis lorem. Integer volutpat elementum ante, a commodo enim vulputate vitae. Nullam enim justo, maximus sed ex in, fringilla auctor libero. Quisque efficitur dui vel libero semper commodo. Vestibulum ornare cursus mattis. Mauris commodo porttitor pellentesque. Aenean efficitur neque elementum mi feugiat consequat.
          </p>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'TempNdviText',
    data() {
      return {
        //
      }
    }
  }
  </script>
  
  <style scoped>
  .temp-ndvi-text-section {
    margin: 50px 0;
    text-align: center;
  }
  
  .temp-ndvi-text {
    font-size: 1.2rem;
    font-weight: 300;
  }
  </style>
  
<template>
    <v-container class="ndvi-text-section" fluid>
      <v-row justify="center">
        <v-col cols="12" md="10">
          <p style="font-weight: 600; font-size: 1.4rem">
            NDVI: What is it and why is it relevant?
          </p>
          <p class="ndvi-text pt-10">
            NDVI is a satellite-derived metric used for quantifying the health of vegetation. NDVI is calculated by measuring the difference between light that is reflected and light that is absorbed. Healthy plants (chlorophyll) reflect a lot of near-infrared (NIR) light and absorb red light, while less healthy or sparse vegetation reflects less NIR light and absorbs less red light. NDVI values range from -1 to +1, where higher numbers indicate healthier, denser vegetation that has low reflectance in the red channel and high reflectance in the NIR channel.          </p>
          <p class="ndvi-text pt-6" style="font-weight: 600;">
            NDVI = (NIR-RED) / (NIR+RED)
          </p>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'NdviText',
    data() {
      return {
        //
      }
    }
  }
  </script>
  
  <style scoped>
  .ndvi-text-section {
    margin: 50px 0;
    text-align: center;
  }
  
  .ndvi-text {
    font-size: 1.2rem;
    font-weight: 300;
  }
  </style>
  
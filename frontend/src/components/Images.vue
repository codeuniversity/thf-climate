<template>
    <v-container class="pb-16">
      <v-row justify="center">
        <v-col class="text-center">
          <img src="@/assets/images/sentinel-2-l2a-thf-2022-03-22.png" alt="">
        </v-col>
        <v-col class="text-center">
          <img src="@/assets/images/sentinel-2-l2a-thf-2023-05-08.png" alt="">
        </v-col>
      </v-row>
      <p class="py-6">
        Sentinel-2 images of Tempelhofer Feld before the growing season (22.03.2022, left) and during the growing season (08.05.2023, right) with very healthy vegetation.
      </p>
      <v-row justify="center">
        <v-col class="text-center">
          <img src="@/assets/images/ndvi-thf-2022-05-08.png" alt="">
        </v-col>
        <v-col class="text-center">
          <img src="@/assets/images/ndvi-thf-2023-05-08.png" alt="">
        </v-col>
      </v-row>
      <p class="py-6">
        NDVI of Tempelhofer Feld for the same satellite images above (22.03.2022, left; 08.05.2023, right). Lighter shades of green indicate low NDVI, while darker shades indicate higher NDVI.
      </p>
    </v-container>
  </template>
  
  <script>
  
  </script>
  
  <style scoped>
  img {
    width: 450px;
    padding: 15px;
  }

  p {
    margin: 0;
    font-size: 1.2rem;
    font-weight: 300;
  }
  </style>
  
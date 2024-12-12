<template>
  <v-app>
    <v-container fluid>
      <!-- Temperature Section -->
      <v-row>
        <v-col :cols="4">
          <section>
            <h4>Temperature</h4>
            <p>
              This section provides insights into temperature trends and variations. 
              Add detailed descriptions and key findings related to temperature data here.
            </p>
          </section>
        </v-col>

        <v-col :cols="8">
          <section>
            <v-container>
              <v-img
                src="https://via.placeholder.com/800x400"
                alt="Temperature graph"
                aspect-ratio="16/9"
                class="mb-10"
              ></v-img>
              <v-img
                src="https://via.placeholder.com/800x400"
                alt="Temperature graph"
                aspect-ratio="16/9"
                class="mb-10"
              ></v-img>
              <v-img
                src="https://via.placeholder.com/800x400"
                alt="Temperature graph"
                aspect-ratio="16/9"
              ></v-img>
            </v-container>
          </section>
        </v-col>
      </v-row>

      <!-- NDVI Section -->
      <v-row>
        <v-col :cols="4">
          <section>
            <h4>NDVI</h4>
            <p>
              This section explores NDVI (Normalized Difference Vegetation Index) and its implications. 
              Provide context, observations, and any interesting patterns identified.
            </p>
          </section>
        </v-col>

        <v-col :cols="8">
          <section>
            <v-container>
              <v-img
                src="https://via.placeholder.com/800x400"
                alt="NDVI image"
                aspect-ratio="16/9"
                class="mb-10"
              ></v-img>
              <v-img
                src="https://via.placeholder.com/800x400"
                alt="NDVI image"
                aspect-ratio="16/9"
                class="mb-10"
              ></v-img>
              <v-img
                src="https://via.placeholder.com/800x400"
                alt="NDVI image"
                aspect-ratio="16/9"
              ></v-img>
            </v-container>
          </section>
        </v-col>
      </v-row>

      <!-- NDVI Graph Section -->
      <v-row>
        <v-col :cols="4">
          <section>
            <h4>NDVI Graphs</h4>
            <p>
              This section explores NDVI graphs and their significance.
            </p>
          </section>
        </v-col>

        <v-col :cols="8">
          <section>
            <v-container>
              <v-img
                src="https://via.placeholder.com/800x400"
                alt="NDVI graph"
                aspect-ratio="16/9"
                class="mb-10"
              ></v-img>
              <v-img
                src="https://via.placeholder.com/800x400"
                alt="NDVI graph"
                aspect-ratio="16/9"
                class="mb-10"
              ></v-img>
              <v-img
                src="https://via.placeholder.com/800x400"
                alt="NDVI graph"
                aspect-ratio="16/9"
              ></v-img>
            </v-container>
          </section>
        </v-col>
      </v-row>

      <!-- Temperature vs. NDVI Section -->
      <v-row>
        <v-col :cols="4">
          <section>
            <h4>Temperature vs. NDVI</h4>
            <p>
              This section analyzes the relationship between temperature and NDVI. 
              Discuss correlations, trends, and any relevant insights derived from the data.
            </p>
          </section>
        </v-col>

        <v-col :cols="8">
          <section>
            <v-container>
              <v-img
                src="https://via.placeholder.com/800x400"
                alt="Temperature vs. NDVI graph"
                aspect-ratio="16/9"
                class="mb-10"
              ></v-img>
              <v-img
                src="https://via.placeholder.com/800x400"
                alt="Temperature vs. NDVI graph"
                aspect-ratio="16/9"
                class="mb-10"
              ></v-img>
              <v-img
                src="https://via.placeholder.com/800x400"
                alt="Temperature vs. NDVI graph"
                aspect-ratio="16/9"
              ></v-img>
            </v-container>
          </section>
        </v-col>
      </v-row>

      <!-- Conclusion -->
      <v-row>
        <v-col :cols="4">
          <section>
            <h4>Conclusion</h4>
            <p>
              This section provides a summary of key findings and conclusions drawn from the data analysis.
            </p>
          </section>
        </v-col>

        <v-col :cols="8">
          <section>
            <v-container>
              <v-img
                src="https://via.placeholder.com/800x400"
                alt="Tempelhofer Feld"
                aspect-ratio="16/9"
              ></v-img>
            </v-container>
          </section>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
export default {
  name: "MainSection",
  data() {
    return {
      //
    }
  },
}
</script>

<style scoped>
section {
  margin-bottom: 16px;
}

p {
  font-size: 1.2rem;
  font-weight: 300;
  line-height: 1.5;
}
</style>

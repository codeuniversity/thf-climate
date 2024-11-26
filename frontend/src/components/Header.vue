<template>
  <v-container class="header-container pa-0" fluid>
    <img src="@/assets/images/Berlin_Tempelhofer_Feld_UAV_05-2017.jpg" class="header-image">
      <div class="overlay">
        <h1 class="title">Climates of Tempelhofer Feld</h1>
        <h2 class="subtitle">A data visualization project</h2>
        <v-btn icon density="comfortable">
          <v-icon>mdi-chevron-down</v-icon>
        </v-btn>
      </div>
    </img>
  </v-container>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      //
    }
  }
}
</script>

<style scoped>
.header-container {
  position: relative;
}

.header-image {
  height: 100vh;
  width: 100%;
  object-fit: cover;
  object-position: center;
}

.overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
}

.title {
  font-weight: bold;
}

.subtitle {
  padding: 20px 0;
  font-size: 1.5rem;
  font-weight: 300;
}
</style>

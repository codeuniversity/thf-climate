<template>
  <v-container class="header-container pa-0 mb-0" fluid>
    <img src="@/assets/images/Berlin_Tempelhofer_Feld_UAV_05-2017.jpg" class="header-image">
      <div class="overlay">
        <h1 class="title">Climates of Tempelhofer Feld</h1>
        <h2 class="subtitle">An Earth Observation Project</h2>
        <v-btn icon density="comfortable" @click="scrollToIntro">
          <v-icon>mdi-chevron-down</v-icon>
        </v-btn>
      </div>
    </img>
  </v-container>
</template>

<script>
import { onMounted } from 'vue'

export default {
  name: 'Header',
  setup() {
    const scrollToIntro = () => {
      const introSection = document.getElementById('introduction-section')
      if (introSection) {
        introSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }

    onMounted(() => {
      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            scrollToIntro()
          }
        },
        {
          threshold: 0.5,
        }
      );
      
      const introSection = document.getElementById('introduction-section')
      if (introSection) {
        observer.observe(introSection)
      }
    })

    return {
      scrollToIntro
    }
  }
}
</script>

<style scoped>
.header-container {
  position: relative;
  padding: 0;
  margin: 0;
  height: 100vh;
}

.header-image {
  height: 100%;
  width: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
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
  font-size: 3.5rem;
}

.subtitle {
  padding: 20px 0;
  font-size: 1.5rem;
  font-weight: 300;
}
</style>

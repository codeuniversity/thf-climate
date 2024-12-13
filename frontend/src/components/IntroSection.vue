<template>
  <v-container class="introduction-section pb-16" fluid id="introduction-section">
    <v-row justify="center">
      <v-col cols="12" md="10" class="pt-10">
        <p style="font-weight: 600; font-size: 1.4rem">
          The climate is changing, and so is the vegetation at Berlin’s beloved Tempelhofer Feld.
        </p>
        <p class="intro-text pt-10">
          Climate change affects the entire globe, but its impacts are also evident on a smaller, local scale. Tempelhofer Feld, a unique urban oasis in Berlin, serves as an example of this. Once an airport in the middle of the city, this vast field has transformed into a public park, offering a fascinating case study of how urban green spaces evolve and respond to changes in climate.
        </p>
        <p class="intro-text pt-6">
          We analyzed the microclimate of this unique area by deriving vegetation indices from high-resolution satellite imagery and utilizing long-term in-vitro sensors.
        </p>
        <p class="intro-text pt-6">
          Check out the results yourself below.
        </p>

        <div class="navigation-links pt-4">
          <div @click="toggleNavigation" class="toggle-header">
            <span>{{ isNavigationOpen ? '▼' : '►' }}</span>
            Quick Navigation 
          </div>
          <ul v-if="isNavigationOpen" class="toggle-list">
            <li><a href="#temperature-section">Temperature</a></li>
            <li><a href="#ndvi-explanation-section">What is NDVI</a></li>
            <li><a href="#ndvi-results-section">NDVI</a></li>
            <li><a href="#correlations-section">Correlations</a></li>
            <li><a href="#conclusion-section">Conclusion</a></li>
            <li><a href="#about-section">About</a></li>
          </ul>
        </div>

        <v-row justify="center" align="center" class="pt-10" dense>
          <v-col cols="12" md="5" class="d-flex flex-column align-items-center my-6 mx-4">
            <img 
              src="@/assets/images/snow-thf-dec-2010.png" 
              alt="Several centimeters of snow and people cross country skiing on Tempelhofer Feld" 
              class="image"
            />
            <p class="caption">
              <a href="https://www.flickr.com/people/29949005@N02/">© Berlin-Knipser</a>
            </p>
          </v-col>
          <v-col cols="12" md="5" class="d-flex flex-column align-items-center mx-4">
            <img 
              src="@/assets/images/no-snow-thf-dec-2024.png" 
              alt="People enjoying Tempelhofer Feld"
              class="image"
            />
            <p class="caption">
              <a href="https://www.flickr.com/people/gojade/">© Jan Gold</a>
            </p>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'IntroSection',
  data() {
    return {
      isNavigationOpen: false,
    }
  },
  methods: {
    toggleNavigation() {
      this.isNavigationOpen = !this.isNavigationOpen;
    },
    scrollToTemperature() {
      const temperatureSection = document.getElementById('temperature-section')
      if (temperatureSection) {
        temperatureSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }
  },
  mounted() {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          this.scrollToTemperature()
        }
      },
      {
        threshold: 0.5,
      }
    );
    
    const temperatureSection = document.getElementById('temperature-section')
    if (temperatureSection) {
      observer.observe(temperatureSection)
    }
  }
}
</script>

<style scoped>
.introduction-section {
  text-align: center;
  background-color: #e8fae6;
}

.intro-text {
  font-size: 1.2rem;
  font-weight: 300;
}

.navigation-links {
  margin: 20px 0;
  font-weight: 600;
  cursor: pointer;
}

.toggle-list {
  list-style-type: none;
  margin: 10px 0 0;
  padding: 0;
}

.toggle-list li {
  margin: 5px 0;
}

.toggle-list li a {
  text-decoration: none;
  color: #007BFF;
  font-weight: 400;
}

.toggle-list li a:hover {
  text-decoration: underline;
}

.image {
  max-width: 100%;
  height: auto;
}

.caption {
  font-size: 0.9rem;
  color: #555;
  text-align: center;
  margin-top: 0.5rem;
}
</style>

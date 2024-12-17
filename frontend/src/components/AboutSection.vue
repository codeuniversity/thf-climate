<template>
  <v-container id="about-section" class="about-section pt-16" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <h3>A CODE University Professor-led Project</h3>
        <p class="about-text pt-4">
          This project was conducted as part of a professor-led semester Project
          at CODE University of Applied Sciences. Our team aimed to explore the
          unique urban ecosystem of Tempelhofer Feld and its response to
          changing climatic conditions. The findings presented on this site are
          only a fraction of the work we carried out.
        </p>
        <p class="about-text pt-4">
          In addition to analyzing NDVI, we explored other vegetation indices
          like MSAVI and GNDVI, as well as in-vitro measurements such as air
          humidity and soil moisture. We also explored data from other remote
          sensing sources, including SAR imagery.
        </p>
        <p class="about-text pt-4">
          To manage and query these insights in real time, we developed a robust
          infrastructure supported by caching strategies to ensure optimal
          performance. This system enables dynamic exploration of the data and
          supports future scalability.
        </p>
        <p class="about-text pt-4">
          The success of this project was made possible by the collaborative
          efforts of our team members:
        </p>
        <ul class="pt-4">
          <li>Essam Ali</li>
          <li>Abdul Sanni</li>
          <li>Till Ermold</li>
          <li>Tom Lustig</li>
          <li>Jules Morley</li>
          <li>Péter T. Winkler</li>
        </ul>
        <p class="about-text pt-4 pb-6">
          And, of course, a huge thank you goes out to Prof. Dr. Adam Roe for
          coming up with the idea for the project and guiding us along the way.
        </p>
        <p class="about-text pt-4 pb-6">
          Looking ahead, we hope this work inspires further studies and
          applications in urban climate resilience.
        </p>
        <p class="about-text pt-4">
          Github Repository:
          <br />
          <a href="https://github.com/codeuniversity/thf-climate"
            >https://github.com/codeuniversity/thf-climate</a
          >
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "AboutSection",
  data() {
    return {
      //
    }
  },
}
</script>

<style scoped>
.about-section {
  text-align: center;
  background-color: #e8fae6;
}

.about-text {
  font-size: 1.2rem;
  font-weight: 300;
}

li {
  list-style-type: none;
}
</style>

<template>
  <v-app>
    <v-container fluid class="pa-3">
      <!-- Temperature Section -->
      <div class="section" id="temperature-section">
        <v-row>
          <v-col :cols="4" class="left-column sticky-left">
            <section :class="{ active: activeSection === 'temperature-section' }">
              <h3 class="pb-4">Temperature</h3>
              <p>
                Over the years, temperatures have shown an overall increase, a clear indicator of climate change. This trend is evident when we look at the historical data of Tempelhofer Feld.
              </p>
              <p class="pt-6">
                The second graph on the right shows average (also called “mean”) temperatures from 1990 to 2008 and how other years differ. Longer red bars indicate warmer years; longer blue bars indicate cooler years. Tempelhof Airport closed in 2008 so that year marks the end of the reference period. Understanding these differences helps us see climate change patterns and impacts. August shows the most extreme deviations.
              </p>

              <!-- TODO: -->
              <!-- <p class="pt-6">
                [move month select for difference graph here]
              </p> -->
            </section>
          </v-col>

          <v-col :cols="8">
            <section>
              <v-container>
                <MedianTempGraph />
                <TempDifferenceGraph />
              </v-container>
            </section>
          </v-col>
        </v-row>
      </div>

      <!-- NDVI Section -->
      <div class="section" id="ndvi-explanation-section">
        <v-row>
          <v-col :cols="4" class="left-column sticky-left">
            <section :class="{ active: activeSection === 'ndvi-explanation-section' }">
              <h3 class="pb-4">NDVI Explanation</h3>
              <p>
              We chose to look at the health of the plant life on the field (we'll refer to this as "vegetation"). One way to understand the health of vegetation on a large area of land is to look at satellite pictures of it. Or, more precisely, using vegetation indices. These are various combinations of the different wavelengths ("colors") that satellites record. The most notable one is the normalized difference vegetation index or NDVI.
            </p>
            <p class="pt-6">
              This index is used to measure the presence and health of vegetation in geographic and ecological surveys, as well as agricultural monitoring. Generally, the higher the NDVI, the healthier and denser the vegetation in the area. The value falls between 1 and -1, where 1 means dense and alive vegetation; values around 0 might indicate the lack of vegetation, like concrete, stone, or snow, while negative values close to -1 usually mean water bodies. 
            </p>
            <p class="pt-6">
              <i>In short, the higher the NDVI, the greener the field.</i>
            </p>
            <p class="pt-6">
              NDVI is the most commonly used vegetation index because it provides a simple yet effective measure of vegetation health and density, leveraging differences in how vegetation reflects near-infrared and visible light.
            </p>
            <p class="pt-6">
              We get our satellite imagery from Google Earth Engine, which gives us access to collections of geographical and satellite information. We use a Python server to retrieve and process the satellite data; you can see a visualization of the NDVI overlaid on a map of Tempelhofer Feld here on the right.
            </p>
            
            <div class="expandable-section pt-6">
              <div @click="toggleExpand" class="toggle-expand">
                <span>{{ isExpanded ? '▼' : '►' }}</span>
                NDVI Calculation 
              </div>
              <p v-if="isExpanded" class="expanded-section pt-4">
                NDVI is calculated by measuring the difference between light that is reflected and light that is absorbed. Healthy plants (chlorophyll) reflect a lot of near-infrared (NIR) light and absorb red light, while less healthy or sparse vegetation reflects less NIR light and absorbs less red light. NDVI values range from -1 to +1, where higher numbers indicate healthier, denser vegetation that has low reflectance in the red channel and high reflectance in the NIR channel.
                <br/>
                <br/>
                Equation: <strong>NDVI = (NIR-RED) / (NIR+RED)</strong>
              </p>
            </div>
            </section>
          </v-col>

          <v-col :cols="8">
            <section>
              <v-container>
                <Images />
              </v-container>
            </section>
          </v-col>
        </v-row>
      </div>

      <!-- NDVI Graph Section -->
      <div class="section" id="ndvi-results-section">
        <v-row>
        <v-col :cols="4" class="left-column sticky-left">
          <section :class="{ active: activeSection === 'ndvi-results-section' }">
            <h3 class="pb-4">NDVI Results</h3>
            <p>
              Our observations of NDVI values across the study area generally ranged between 0.2 and 0.7. One of the lowest recorded values was in December 2018, with an NDVI of 0.1706, while one of the highest was in November 2022, with an NDVI of 0.7010. The data we collected could be improved with more cleaning, as the area includes large concrete sections, is roughly defined, and contains inconsistencies due to changes in land use and purpose over time (like creating the gardening area and introducing sheep).
            </p>
            <p class="pt-6">
              Initially, we expected the NDVI to decline over the years due to increased drought and higher summer temperatures. However, our observations show that the NDVI has been rising on average. While we cannot confidently say why, it is likely driven by shorter, milder winters and longer growing seasons.
            </p>

            <!-- TODO: -->
            <!-- <p class="pt-6">
              [move month select for NDVI graph here]
            </p> -->
          </section>
        </v-col>

        <v-col :cols="8">
          <section>
            <v-container>
              <YearlyNdviPlot />
              <NdviSelectMonthGraph />
              <NdviOverlayGraph />
            </v-container>
          </section>
        </v-col>
      </v-row>
      </div>
      

      <!-- Temperature vs. NDVI Section -->
      <div class="section" id="correlations-section">
        <v-row>
        <v-col :cols="4" class="left-column sticky-left">
          <section :class="{ active: activeSection === 'correlations-section' }">
            <h3 class="pb-4">Understanding the Dynamics of Tempelhofer Feld’s Temperature and Vegetation</h3>
            <p>
              The graph on the right illustrates two critical metrics: the yearly mean temperature and the yearly mean NDVI (in general, reflecting the health and density of plant life). 
            </p>
            <p class="pt-6">
              The graph reveals a striking similarity between the temperature trends and NDVI values. This suggests that temperature is a major driver influencing vegetation health and density.
            </p>
            <p class="pt-6" style="font-weight: 600;">
              What does this mean?
            </p>
            <p class="pt-6">
              Higher temperatures during growing seasons likely extend the vegetation period, leading to higher NDVI values. Conversely, cooler years may result in reduced vegetative activity, reflected in lower NDVI values.
            </p>
            <p class="pt-6">
              This correlation highlights the sensitivity of urban vegetation to temperature fluctuations. While increased temperatures might initially enhance vegetation growth, prolonged warming trends could stress plants, especially during extreme heatwaves or drought periods. Additionally, one must be cautious in interpreting higher NDVI values in warmer years as an indication of healthier vegetation. The absence of snow, which has a very low NDVI, reduces its influence on the yearly average, thereby driving NDVI values higher in such years.
            </p>
          </section>
        </v-col>

        <v-col :cols="8">
          <section>
            <v-container>
              <YearlyTemperatureNdviCorrelation />
            </v-container>
          </section>
        </v-col>
      </v-row>
      </div>

      <!-- Conclusion -->
      <div class="section" id="conclusion-section">
        <v-row>
        <v-col :cols="4" class="left-column sticky-left pb-16">
          <section :class="{ active: activeSection === 'correlations-section' }">
            <h3 class="pb-4">What We Learned and What Comes Next</h3>
            <p>
              The analysis underscores the growing significance of earth observation tools, like satellite imagery and NDVI metrics, in monitoring urban green spaces such as Tempelhofer Feld. These tools provide insights into how ecosystems respond to climate change and enable data-driven decision-making for urban planning and conservation.
            </p>
            <p class="pt-6">
              Earth observation is able to address the challenges of climate monitoring. The consistent and large-scale coverage offered by satellites allows us to track changes over time and across regions.
            </p>
            <p class="pt-6">
              However, we must recognize that this approach is inherently limited when examining the past. High-resolution imagery and tools like NDVI have only become widely available in recent decades, restricting our ability to study long-term historical trends.
            </p>
          </section>
        </v-col>

        <v-col :cols="8">
          <section>
            <v-container>
              <img
                src="@/assets/images/thf-sunset.jpg"
                alt="Tempelhofer Feld at sunset"
                style="width: 100%;"
              />
            </v-container>
          </section>
        </v-col>
      </v-row>
      </div>
    </v-container>
  </v-app>
</template>

<script>
import MedianTempGraph from './WeatherGraphs/MedianTempGraph.vue';
import TempDifferenceGraph from './WeatherGraphs/TempDifferenceGraph.vue';
import Images from './Images.vue';
import YearlyNdviPlot from './NdviGraphs/YearlyNdvi.vue';
import NdviSelectMonthGraph from './NdviGraphs/NdviSelectMonthGraph.vue';
import NdviOverlayGraph from './NdviGraphs/NdviOverlayGraph.vue';
import YearlyTemperatureNdviCorrelation from './CorrelationGraphs/YearlyTemperatureNdviCorrelation.vue';

export default {
  name: 'MainSection',
  components: {
    MedianTempGraph,
    TempDifferenceGraph,
    Images,
    YearlyNdviPlot,
    NdviSelectMonthGraph,
    NdviOverlayGraph,
    YearlyTemperatureNdviCorrelation,
  },
  data() {
    return {
      activeSection: null,
      isExpanded: false,
    };
  },
  methods: {
    toggleExpand() {
      this.isExpanded = !this.isExpanded
    },
  },
  mounted() {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            this.activeSection = entry.target.id;
          }
        });
      },
      { threshold: 0.5 }
    );

    const sections = document.querySelectorAll('.section');
    sections.forEach((section) => observer.observe(section));
  },
};
</script>

<style scoped>
section {
  margin: 16px;
}

p {
  font-weight: 300;
  line-height: 1.5;
}

.left-column {
  background-color: #d6f5d3;
}


.sticky-left {
  position: sticky;
  top: 0px;
  height: fit-content;
  align-self: flex-start;
}
</style>

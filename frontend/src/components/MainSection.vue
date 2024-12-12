<template>
  <v-app>
    <v-container fluid class="pa-3">
      <!-- Temperature Section -->
      <v-row>
        <v-col :cols="4" class="left-column">
          <section>
            <h3 class="pb-4">Temperature</h3>
            <p>
              [insert intro to temperature section - mention first graph]
            </p>
            <p class="pt-6">
              The second graph on the right shows average temperatures from 1990 to 2008 and how other years differ. Taller red bars indicate warmer years; taller blue bars indicate cooler years. Tempelhof Airport closed in 2008, so that year marks the end of the reference period. Understanding these differences helps us see climate change patterns and impacts. August shows the most extreme deviations. Select any month from the drop-down to see its temperature deviations.
            </p>
            <p class="pt-6">
              [move month select for difference graph here]
            </p>
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

      <!-- NDVI Section -->
      <v-row>
        <v-col :cols="4" class="left-column">
          <section>
            <h3 class="pb-4">NDVI</h3>
            <p>
              We chose to look at the health of the plant life on the field (we'll refer to this as "vegetation"). One way to understand the health of vegetation on a large area of land is to look at satellite pictures of it. Or more specifically: using vegetation indices. These are various combinations of the different wavelengths ("colors") that satellites record. The most notable one: Normalized difference vegetation index or NDVI.
            </p>
            <p class="pt-6">
              This index is used to measure the presence and health of vegetation. Generally the higher the NDVI the healthier and more dense the vegetation is in the area. The value falls between 1 and -1 where 1 means dense and alive vegetation, values around 0 might indicate the lack of vegetation, like concrete, stone or snow, while negative values close to -1 usually mean water bodies. In short, the higher the NDVI, the greener the field.
            </p>
            <p class="pt-6">
              NDVI is the most commonly used vegetation index because it provides a simple yet effective measure of vegetation health and density, leveraging differences in how vegetation reflects near-infrared and visible light.
            </p>
            <p class="pt-6">
              [Insert expandable section on NDVI in-depth]
            </p>
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

      <!-- NDVI Graph Section -->
      <v-row>
        <v-col :cols="4" class="left-column">
          <section>
            <h3 class="pb-4">NDVI Results</h3>
            <p>
              Our observations of NDVI values across the study area generally ranged between 0.2 and 0.7. One of the lowest recorded values was in December 2018, with an NDVI of 0.1706, while one of the highest was in November 2022, with an NDVI of 0.7010. The data we collected is not very clean, as the area includes large sections of concrete, is roughly defined, and contains inconsistencies due to changes in land use and purpose over time.
            </p>
            <p class="pt-6">
              Initially, we expected the NDVI to decline over the years due to increased drought and higher summer temperatures. However, our observations show that the NDVI has been rising on average, likely driven by shorter and milder winters and longer growing seasons.
            </p>
            <p class="pt-6">
              [move month select for NDVI graph here]
            </p>
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

      <!-- Temperature vs. NDVI Section -->
      <v-row style="height: 100vh;">
        <v-col :cols="4" class="left-column">
          <section>
            <h3 class="pb-4">Understanding the Dynamics of Tempelhofer Feld’s Temperature and Vegetation</h3>
            <p>
              The graph on the right illustrates two critical metrics: the yearly mean temperature and the yearly mean NDVI (In general reflecting the health and density of plant life). 
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
              This correlation highlights the sensitivity of urban vegetation to temperature fluctuations. While increased temperatures might initially enhance vegetation growth, prolonged warming trends could stress plants, especially during extreme heatwaves or drought periods. Additionally, one must be cautious in interpreting higher NDVI values in warmer years as an indication of healthier vegetation. The absence of snow, which has very low NDVI, reduces its influence on the yearly average, thereby driving NDVI values higher in such years.
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

      <!-- Conclusion -->
      <v-row style="height: 100vh;">
        <v-col :cols="4" class="left-column pb-16">
          <section>
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
    </v-container>
  </v-app>
</template>

<script>
import YearlyTemperatureNdviCorrelation from './CorrelationGraphs/YearlyTemperatureNdviCorrelation.vue'
import MedianTempGraph from './WeatherGraphs/MedianTempGraph.vue'
import TempDifferenceGraph from './WeatherGraphs/TempDifferenceGraph.vue'
import Images from './Images.vue'
import YearlyNdviPlot from './NdviGraphs/YearlyNdvi.vue'
import NdviSelectMonthGraph from './NdviGraphs/NdviSelectMonthGraph.vue'
import NdviOverlayGraph from './NdviGraphs/NdviOverlayGraph.vue'

export default {
  name: "MainSection",
  components: {
    MedianTempGraph,
    TempDifferenceGraph,
    YearlyTemperatureNdviCorrelation,
    Images,
    YearlyNdviPlot,
    NdviSelectMonthGraph,
    NdviOverlayGraph,
  },
  data() {
    return {
      //
    }
  },
}
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
  background-color: #c0e8bc;
}
</style>

<template>
  <v-container class="introduction-section" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <h3>Introduction</h3>
        <p class="intro-text pt-4">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Suspendisse id suscipit nulla, ac commodo ex. Nunc finibus semper nulla a pharetra.
            Ut lobortis, mi sit amet eleifend iaculis, velit justo lobortis nisi, ac lobortis lacus ante nec nisi.
            Etiam pulvinar imperdiet quam. Pellentesque ipsum dolor, lobortis vel sapien id, tincidunt finibus massa.
            Vestibulum sollicitudin dictum lacus, non sagittis augue consectetur id.
            Nulla sed mauris gravida, mattis enim quis, aliquam lacus.
            Sed iaculis nunc dui, et rutrum erat pellentesque placerat.
            Integer eu nulla imperdiet, scelerisque odio at, interdum tellus.
            Sed porttitor odio in lacinia posuere.
            Quisque ultricies condimentum massa quis placerat.
            Nulla tempor nisi id odio convallis rutrum.
            Vestibulum felis ante, tincidunt et venenatis id, consectetur at quam.
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'IntroSection',
  data() {
    return {
      //
    }
  }
}
</script>

<style scoped>
.introduction-section {
  margin: 50px 0;
  text-align: center;
}

.intro-text {
  font-size: 1.2rem;
  font-weight: 300;
}
</style>

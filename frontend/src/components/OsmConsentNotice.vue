<template>
  <v-container class="osm-consent-notice">
    <p class="osm-consent-notice__text">
      You have declined the use of OpenStreetMap as the background map.
    </p>
    <v-btn small class="osm-consent-notice__button" @click="showAgain">
      Show again
    </v-btn>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class OsmConsentNotice extends Vue {
  public showAgain() {
    localStorage.removeItem("osmConsent");
    this.$root.$emit("update_osm_consent");
  }
}
</script>

<style scoped>
.osm-consent-notice {
  position: absolute;
  bottom: 2rem;
  left: 0;
  right: 0;
  max-width: 500px;
  background-color: white;
  color: black;
  margin: 0 auto;
  padding: 1rem;
  border-radius: 0.25rem;
  font-size: 9pt;
}
.osm-consent-notice__text {
  margin: 0;
}
.osm-consent-notice__button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  margin: 1rem auto;
}

@media (min-width: 992px) {
  .osm-consent-notice {
    display: flex;
  }
  .osm-consent-notice__button {
    margin: auto 0;
  }
}
</style>

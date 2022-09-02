<template>
  <l-map style="z-index: 0">
    <l-tile-layer :url="urlOSM" :attribution="attributionOSM"></l-tile-layer>
    <l-tile-layer :url="urlOWM" :attribution="attributionOWM"></l-tile-layer>
    <l-marker v-if="currentPosition" :lat-lng="currentPosition"></l-marker>
  </l-map>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { api } from "@/api";

@Component
export default class Map extends Vue {
  public urlOSM = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
  public get urlOWM() {
    return api.getTilesEndpoint();
  }
  public attributionOSM =
    "&copy; <a href=\"http://osm.org/copyright\">OpenStreetMap</a> contributors";
  public attributionOWM = "TODO";
  public get currentPosition() {
    if (
      this.$store.state.geolocation.lat &&
      this.$store.state.geolocation.lng
    ) {
      return [
        this.$store.state.geolocation.lat,
        this.$store.state.geolocation.lng,
      ];
    } else {
      return null;
    }
  }
}
</script>

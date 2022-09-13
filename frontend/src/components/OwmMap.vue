<template>
  <l-map
    ref="owmMap"
    style="z-index: 0"
    :zoom="zoom"
    :center="center"
    @ready="mapReady"
  >
    <l-tile-layer :url="urlOSM" :attribution="attributionOSM"></l-tile-layer>
    <l-marker v-if="currentPosition" :lat-lng="currentPosition"></l-marker>
  </l-map>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { api } from "@/api";
import L from "leaflet";
import { LMap } from "vue2-leaflet";
import { appVersion } from "@/env";

@Component
export default class OwmMap extends Vue {
  public owmMap?: L.Map;
  public owmTileLayer?: L.TileLayer;
  public zoom = 11;
  public center = [52.5183, 13.4006];
  public urlOSM = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
  public attributionOSM =
    '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors';
  public attributionOWM = "TODO " + appVersion;
  public urlOWM() {
    // adding random characters to the end
    // will prevent browser from caching tiles
    // the random string is updated only when a new sample is added
    // to force a reload of the tiles
    return `${api.getTilesEndpoint()}?${Math.random()}`;
  }
  public refreshOwmMap() {
    this.owmTileLayer?.setUrl(this.urlOWM());
  }
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
  public mounted() {
    this.$root.$on("refresh_owm_map", () => {
      this.refreshOwmMap();
    });
  }
  public mapReady() {
    this.owmMap = (this.$refs.owmMap as LMap).mapObject;
    this.owmTileLayer = L.tileLayer(this.urlOWM(), {attribution: this.attributionOWM});
    this.owmTileLayer.addTo(this.owmMap);
  }
}
</script>

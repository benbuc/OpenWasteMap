<template>
  <l-map
    ref="owmMap"
    style="z-index: 0"
    :zoom="zoom"
    :center="center"
    @ready="mapReady"
    @update:center="centerUpdate"
    @update:zoom="zoomUpdate"
  >
    <l-tile-layer :url="urlOSM" :attribution="attributionOSM"></l-tile-layer>
    <l-marker v-if="currentPosition" :lat-lng="currentPosition"></l-marker>
  </l-map>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { api } from "@/api";
import L, { latLng } from "leaflet";
import { LMap } from "vue2-leaflet";
import { appVersion } from "@/env";

@Component
export default class OwmMap extends Vue {
  public owmMap?: L.Map;
  public owmTileLayer?: L.TileLayer;
  public zoom = 11;
  public center = latLng(52.5183, 13.4006);
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
  public centerUpdate(center) {
    this.center = center;
  }
  public zoomUpdate(zoom) {
    this.zoom = zoom;
    // zoom update is also triggered on center update
    // update url only once
    this.updateUrl();
  }
  public updateUrl() {
    history.replaceState(
      null,
      "",
      `/@${this.center.lat.toFixed(5)},${this.center.lng.toFixed(5)},${
        this.zoom
      }z`
    );
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
  public created() {
    if (this.$route.params.view_center_zoom) {
      const viewRegExp = new RegExp(/^@([\d\.]+),([\d\.]+),(\d+)z*$/g);
      const view = viewRegExp.exec(this.$route.params.view_center_zoom)!;
      this.zoom = Number(view[3]);
      this.center = latLng(Number(view[1]), Number(view[2]));
    }
  }
  public mounted() {
    this.$root.$on("refresh_owm_map", () => {
      this.refreshOwmMap();
    });
  }
  public mapReady() {
    this.owmMap = (this.$refs.owmMap as LMap).mapObject;
    this.owmTileLayer = L.tileLayer(this.urlOWM(), {
      attribution: this.attributionOWM,
    });
    this.owmTileLayer.addTo(this.owmMap);
  }
}
</script>

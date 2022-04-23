<template>
  <div>
    <v-content v-if="showMap">
      <l-map style="height: 500px">
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <l-tile-layer :url="urlOwm" :attribution="attributionOwm"></l-tile-layer>
      </l-map>
    </v-content>
    <router-view v-else></router-view>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Start extends Vue {
  get showMap() {
    return this.$route.name === 'home';
  }
  public url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
  public urlOwm = 'http://localhost/api/v1/tiles/{z}/{x}/{y}.png';
  public attribution = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors';
  public attributionOwm = 'TODO';
}
</script>

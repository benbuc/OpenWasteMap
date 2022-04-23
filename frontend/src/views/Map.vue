<template>
    <l-map>
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <l-tile-layer :url="urlOwm" :attribution="attributionOwm"></l-tile-layer>
    </l-map>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Map extends Vue {
  public url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
  public urlOwm = 'http://localhost/api/v1/tiles/{z}/{x}/{y}.png';
  public attribution = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors';
  public attributionOwm = 'TODO';
}
</script>
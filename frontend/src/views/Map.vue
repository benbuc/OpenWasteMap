<template>
    <v-content>
    <l-map style="z-index: 0">
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <l-tile-layer :url="urlOwm" :attribution="attributionOwm"></l-tile-layer>
    </l-map>
    <Nav />
    </v-content>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { api } from '@/api';
import Nav from '@/components/Nav.vue';

@Component({
  components: {
    Nav,
  },
})
export default class Map extends Vue {
  public url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
  public get urlOwm() {
    return api.getTilesEndpoint();
  }
  public attribution = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors';
  public attributionOwm = 'TODO';
}
</script>
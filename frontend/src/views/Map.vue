<template>
    <v-content>
      <l-map style="z-index: 0">
          <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
          <l-tile-layer :url="urlOwm" :attribution="attributionOwm"></l-tile-layer>
      </l-map>
      <div class="menu-wrapper">
        <Nav />
        <v-scale-transition>
          <router-view class="router-view" v-if="showDialog"></router-view>
        </v-scale-transition>
      </div>
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
  public get showDialog() {
    return this.$route.name !== 'home';
  }
}
</script>

<style scoped>
.menu-wrapper {
    position: fixed;
    top: 15px;
    right: 15px;
}
.router-view {
  position: absolute;
  right: 0;
  width: min(400px, calc(100vw - 30px));
}
</style>
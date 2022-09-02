<template>
    <v-main>
      <OwmMap />
      <div class="menu-wrapper">
        <Nav />
        <v-scale-transition>
          <router-view class="router-view" v-if="showDialog"></router-view>
        </v-scale-transition>
      </div>
    </v-main>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Nav from '@/components/Nav.vue';
import OwmMap from '../components/OwmMap.vue';

@Component({
  components: {
    Nav,
    OwmMap,
  },
})
export default class Home extends Vue {
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
  width: min(400px, 100vw);
}
.router-view {
  position: absolute;
  right: 0;
  width: calc(100% - 45px);
}
</style>
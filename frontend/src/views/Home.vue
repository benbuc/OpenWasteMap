<template>
    <v-content>
      <OwmMap />
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
}
.router-view {
  position: absolute;
  right: 0;
  width: min(400px, calc(100vw - 30px));
}
</style>
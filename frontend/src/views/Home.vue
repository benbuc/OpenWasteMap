<template>
  <v-main>
    <OwmMap />
    <div class="menu-wrapper">
      <FABProfile />
      <v-scale-transition>
        <router-view class="router-view" v-if="showDialog"></router-view>
      </v-scale-transition>
    </div>
    <FABCreateSample v-if="loggedIn"></FABCreateSample>
  </v-main>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import OwmMap from "../components/OwmMap.vue";
import FABCreateSample from "../components/FABCreateSample.vue";
import { readIsLoggedIn } from "@/store/main/getters";
import { dispatchCheckLoggedIn } from "@/store/main/actions";
import FABProfile from "../components/FABProfile.vue";

@Component({
  components: {
    OwmMap,
    FABProfile,
    FABCreateSample,
  },
})
export default class Home extends Vue {
  public get showDialog() {
    return this.$route.name !== "home";
  }
  get loggedIn() {
    return readIsLoggedIn(this.$store);
  }
  public async mounted() {
    dispatchCheckLoggedIn(this.$store);
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

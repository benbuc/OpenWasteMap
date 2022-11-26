<template>
  <div id="app">
    <v-app>
      <MainMenuDrawer v-model="showDrawer"></MainMenuDrawer>
      <MainMenuButton v-model="showDrawer"></MainMenuButton>
      <NotificationsManager></NotificationsManager>
      <router-view></router-view>
    </v-app>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import NotificationsManager from "@/components/NotificationsManager.vue";
import MainMenuDrawer from "@/components/MainMenuDrawer.vue";
import MainMenuButton from "./components/MainMenuButton.vue";

@Component({
  components: {
    NotificationsManager,
    MainMenuDrawer,
    MainMenuButton,
  },
})
export default class App extends Vue {
  showDrawer = false;

  public mounted() {
    document.body.style.overflow = "hidden";
    window.addEventListener("resize", this.onResize);
  }
  public unmounted() {
    window.removeEventListener("resize", this.onResize);
  }
  onResize() {
    document.body.style.height = window.innerHeight + "px";
  }
}
</script>

<template>
  <div id="app">
    <v-app>
      <MainMenuDrawer v-model="showDrawer"></MainMenuDrawer>

      <v-btn
        v-model="showDrawer"
        app
        fixed
        top
        left
        fab
        dark
        color="primary"
        @click="showDrawer = !showDrawer"
      >
        <v-icon>menu</v-icon>
      </v-btn>

      <NotificationsManager></NotificationsManager>
      <router-view></router-view>
    </v-app>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import NotificationsManager from "@/components/NotificationsManager.vue";
import MainMenuDrawer from "@/components/MainMenuDrawer.vue";

@Component({
  components: {
    NotificationsManager,
    MainMenuDrawer,
  },
})
export default class App extends Vue {
  showDrawer = false;
}
</script>

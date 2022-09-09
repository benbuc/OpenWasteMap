<template>
  <div id="app">
    <v-app>
      <router-view></router-view>
      <NotificationsManager></NotificationsManager>
    </v-app>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import NotificationsManager from "@/components/NotificationsManager.vue";

@Component({
  components: {
    NotificationsManager,
  },
})
export default class App extends Vue {}
</script>

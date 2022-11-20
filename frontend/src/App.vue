<template>
  <div id="app">
    <v-app>
      <NotificationsManager></NotificationsManager>
      <router-view></router-view>
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

<template>
  <div class="buttons-wrapper">
    <v-btn class="mx-2" fab dark :color="buttonColor" :to="buttonLink">
      <v-icon>person</v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { readIsLoggedIn } from "@/store/main/getters";
import { dispatchCheckLoggedIn } from "@/store/main/actions";

@Component
export default class FABProfile extends Vue {
  public get buttonLink() {
    if (readIsLoggedIn(this.$store)) {
      return "/profile";
    } else {
      return this.$route.path !== "/login" ? "/login" : "/";
    }
  }
  public get buttonColor() {
    if (readIsLoggedIn(this.$store)) {
      return "green";
    }
    if (this.$route.path === "/login") {
      return "primary";
    }
    return "grey";
  }
  public async mounted() {
    dispatchCheckLoggedIn(this.$store);
  }
}
</script>

<style scoped>
.buttons-wrapper {
  text-align: right;
  margin-bottom: 10px;
}
</style>

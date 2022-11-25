<template>
  <v-main>
    <v-btn
      fab
      large
      dark
      bottom
      left
      class="v-btn--admin"
      :to="{ name: 'admin' }"
      v-if="userProfile && userProfile.is_superuser"
    >
      <v-icon>admin_panel_settings</v-icon>
    </v-btn>
    <v-btn fab dark top right class="v-btn--to-map" :to="{ name: 'home' }">
      <v-icon>map</v-icon>
    </v-btn>
    <UserProfile></UserProfile>
  </v-main>
</template>

<script lang="ts">
import store from "@/store";
import {
  dispatchCheckLoggedIn,
  dispatchResendEmailVerification,
} from "@/store/main/actions";
import { readIsLoggedIn, readUserProfile } from "@/store/main/getters";
import { Component, Vue } from "vue-property-decorator";
import UserProfile from "./main/profile/UserProfile.vue";

const routeGuardMain = async (to, from, next) => {
  await dispatchCheckLoggedIn(store);
  if (!readIsLoggedIn(store)) {
    next("/login");
  } else {
    next();
  }
};

@Component({
  components: {
    UserProfile,
  },
})
export default class ProfileIndex extends Vue {
  get userProfile() {
    return readUserProfile(this.$store)!;
  }

  public beforeRouteEnter(to, from, next) {
    routeGuardMain(to, from, next);
  }
  public beforeRouteUpdate(to, from, next) {
    routeGuardMain(to, from, next);
  }
}
</script>

<style scoped>
.v-btn--admin {
  bottom: 0;
  position: absolute;
  margin: 0 0 16px 16px;
}
.v-btn--to-map {
  top: 0;
  right: 0;
  position: absolute;
  margin: 16px 16px 0 0;
}
</style>

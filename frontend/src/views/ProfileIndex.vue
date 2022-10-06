<template>
  <v-main>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-card class="ma-3 pa-3 elevation-12">
          <v-card-title primary-title>{{ userProfile.nickname }}</v-card-title>
          <v-card-text>
            <v-alert outlined type="warning" v-if="!userProfile.email_verified">
              E-mail not yet verified
              <v-btn v-on:click="resendVerification"
                >Re-send verification</v-btn
              >
            </v-alert>
          </v-card-text>
        </v-card>
      </v-layout>
    </v-container>
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

const routeGuardMain = async (to, from, next) => {
  await dispatchCheckLoggedIn(store);
  if (!readIsLoggedIn(store)) {
    next("/login");
  } else {
    next();
  }
};

@Component
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

  public async resendVerification() {
    await dispatchResendEmailVerification(this.$store);
  }
}
</script>

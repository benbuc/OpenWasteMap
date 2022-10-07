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
      v-if="userProfile.is_superuser"
    >
      <v-icon>admin_panel_settings</v-icon>
    </v-btn>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-card class="ma-3 pa-3 elevation-12">
          <v-card-title primary-title>
            <div class="headline primary--text">{{ userProfile.nickname }}</div>
          </v-card-title>
          <v-card-text>
            <v-alert icon="info" outlined type="warning" v-if="!userProfile.email_verified">
              E-mail not yet verified
              <v-btn v-on:click="resendVerification" small
                >Re-send</v-btn
              >
            </v-alert>
            <div class="subheading secondary--text text--lighten-2">Email</div>
            <div class="title primary--text text--darken-2">
              {{ userProfile.email }}
              <v-tooltip
                bottom
                color="success"
                v-if="userProfile.email_verified"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-icon color="success" v-bind="attrs" v-on="on">verified</v-icon>
                </template>
                <span>Email is verified</span>
              </v-tooltip>
            </div>
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

<style scoped>
.v-btn--admin {
  bottom: 0;
  position: absolute;
  margin: 0 0 16px 16px;
}
</style>

<template>
  <v-container fluid>
    <v-layout align-center justify-center>
      <v-card class="ma-3 pa-3">
        <v-card-title primary-title>
          <div class="headline primary--text">User Profile</div>
        </v-card-title>
        <v-card-text>
          <v-alert
            icon="info"
            outlined
            type="warning"
            v-if="userProfile && !userProfile.email_verified"
          >
            E-mail not yet verified
            <v-btn v-on:click="resendVerification" small>Re-send</v-btn>
          </v-alert>
          <div class="my-4">
            <div class="subheading secondary--text text--lighten-3">
              Nickname
            </div>
            <div
              class="title primary--text text--darken-2"
              v-if="userProfile && userProfile.nickname"
            >
              {{ userProfile.nickname }}
            </div>
            <div class="title primary--text text--darken-2" v-else>-----</div>
          </div>
          <div class="my-4">
            <div class="subheading secondary--text text--lighten-3">
              Full Name
            </div>
            <div
              class="title primary--text text--darken-2"
              v-if="userProfile && userProfile.full_name"
            >
              {{ userProfile.full_name }}
            </div>
            <div class="title primary--text text--darken-2" v-else>-----</div>
          </div>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-3">Email</div>
            <div
              class="title primary--text text--darken-2"
              v-if="userProfile && userProfile.email"
            >
              {{ userProfile.email }}
              <v-tooltip
                bottom
                color="success"
                v-if="userProfile.email_verified"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-icon color="success" v-bind="attrs" v-on="on"
                    >verified</v-icon
                  >
                </template>
                <span>Email is verified</span>
              </v-tooltip>
            </div>
            <div class="title primary--text text--darken-2" v-else>-----</div>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn to="/profile/edit">Edit</v-btn>
          <v-btn to="/profile/password">Change password</v-btn>
        </v-card-actions>
      </v-card>
    </v-layout>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
import { readUserProfile } from "@/store/main/getters";
import { dispatchResendEmailVerification } from "@/store/main/actions";

@Component
export default class UserProfile extends Vue {
  get userProfile() {
    return readUserProfile(this.$store);
  }

  public async resendVerification() {
    await dispatchResendEmailVerification(this.$store);
  }
}
</script>

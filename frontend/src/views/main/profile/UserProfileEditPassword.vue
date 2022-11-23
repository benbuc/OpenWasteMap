<template>
  <v-container fluid>
    <v-layout align-center justify-center>
      <v-card class="ma-3 pa-3">
        <v-card-title primary-title>
          <div class="headline primary--text">Set Password</div>
        </v-card-title>
        <v-card-text>
          <template>
            <div class="my-3">
              <div class="subheading secondary--text text--lighten-2">User</div>
              <div
                class="title primary--text text--darken-2"
                v-if="userProfile.nickname"
              >
                {{ userProfile.nickname }}
              </div>
              <div class="title primary--text text--darken-2" v-else>
                {{ userProfile.email }}
              </div>
            </div>
            <v-form ref="form">
              <v-text-field
                label="Password"
                type="password"
                ref="password"
                v-model="password1"
                v-validate="'required|min:8'"
                data-vv-name="password"
                data-vv-delay="100"
                :error-messages="errors.first('password')"
              >
              </v-text-field>
              <v-text-field
                label="Confirm Password"
                type="password"
                v-model="password2"
                v-validate="'required|confirmed:password'"
                data-vv-name="password_confirmation"
                data-vv-delay="100"
                data-vv-as="password"
                :error-messages="errors.first('password_confirmation')"
              >
              </v-text-field>
            </v-form>
          </template>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="cancel">Cancel</v-btn>
          <v-btn @click="reset">Reset</v-btn>
          <v-btn @click="submit" :disabled="!valid">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-layout>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
import { IUserProfile, IUserProfileUpdate } from "@/interfaces";
import { readUserProfile } from "@/store/main/getters";
import { dispatchUpdateUserProfile } from "@/store/main/actions";

@Component
export default class UserProfileEdit extends Vue {
  public valid = true;
  public password1 = "";
  public password2 = "";

  get userProfile() {
    return readUserProfile(this.$store) as IUserProfile;
  }

  public reset() {
    this.password1 = "";
    this.password2 = "";
    this.$validator.reset();
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedProfile: IUserProfileUpdate = {};
      updatedProfile.password = this.password1;
      await dispatchUpdateUserProfile(this.$store, updatedProfile);
      this.$router.push("/profile");
    }
  }
}
</script>

<template>
  <v-main>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>Create Account - {{ appName }}</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form v-model="valid" ref="form" lazy-validation>
                <v-text-field
                  label="Nickname"
                  v-model="nickname"
                  required
                ></v-text-field>
                <v-text-field
                  label="Full Name"
                  v-model="fullName"
                ></v-text-field>
                <v-text-field
                  label="E-Mail"
                  v-model="email"
                  v-validate="'required|email'"
                  data-vv-name="email"
                  required
                ></v-text-field>
                <v-layout align-center>
                  <v-flex>
                    <v-text-field
                      type="password"
                      ref="password"
                      label="Set Password"
                      data-vv-name="password"
                      data-vv-delay="100"
                      v-validate="{ required: true }"
                      v-model="password1"
                      :error-messages="errors.first('password')"
                    >
                    </v-text-field>
                    <v-text-field
                      type="password"
                      label="Confirm Password"
                      data-vv-name="password_confirmation"
                      data-vv-delay="100"
                      data-vv-as="password"
                      v-validate="{ required: true, confirmed: 'password' }"
                      v-model="password2"
                      :error-messages="errors.first('password_confirmation')"
                    >
                    </v-text-field>
                  </v-flex>
                </v-layout>
              </v-form>
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn @click="submit" :disabled="!valid"> Create Account </v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { appName } from "@/env";
import { IUserProfileCreate } from "@/interfaces";
import { dispatchCreateUser } from "@/store/admin/actions";

@Component
export default class Signup extends Vue {
  public valid = false;
  public appName = appName;
  public nickname: string = "";
  public fullName: string = "";
  public email: string = "";
  public setPassword = false;
  public password1: string = "";
  public password2: string = "";

  public async submit() {
    if (await this.$validator.validateAll()) {
      const userProfile: IUserProfileCreate = {
        email: this.email,
        nickname: this.nickname,
      };
      if (this.fullName) {
        userProfile.full_name = this.fullName;
      }
      userProfile.password = this.password1;
      const error = await dispatchCreateUser(this.$store, userProfile);
      if (!error) {
        this.$router.push('/profile');
      }
    }
  }
}
</script>

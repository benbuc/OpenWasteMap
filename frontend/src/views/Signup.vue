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
                  v-validate="'required|min:3|max:20|alpha_num'"
                  data-vv-name="nickname"
                  data-vv-delay="100"
                  required
                  :error-messages="errors.first('nickname')"
                ></v-text-field>
                <v-text-field
                  label="E-Mail"
                  v-model="email"
                  v-validate="'required|email'"
                  data-vv-name="email"
                  data-vv-delay="100"
                  required
                  :error-messages="errors.first('email')"
                ></v-text-field>
                <v-layout align-center>
                  <v-flex>
                    <v-text-field
                      label="Set Password"
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
                      v-validate="{ required: true, confirmed: 'password' }"
                      data-vv-name="password_confirmation"
                      data-vv-delay="100"
                      data-vv-as="password"
                      :error-messages="errors.first('password_confirmation')"
                    >
                    </v-text-field>
                  </v-flex>
                </v-layout>
                <v-checkbox
                  v-model="termsAccepted"
                  required
                  :error-messages="
                    errors.has('privacy_policy')
                      ? 'You have to accept the privacy policy to create an account'
                      : ''
                  "
                >
                  <template slot="label">
                    I agree to the&nbsp;<a
                      @click.stop
                      target="_blank"
                      href="/privacy"
                      >Privacy Policy</a
                    >.
                  </template>
                </v-checkbox>
                <input
                  type="checkbox"
                  name="privacy_policy"
                  v-model="termsAccepted"
                  v-validate="'required'"
                  style="display: none"
                  required
                />
              </v-form>
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn @click="submit" :disabled="!valid"> Create Account </v-btn>
            </v-card-actions>
          </v-card>
          <v-container style="margin-top: 10px">
            <v-row justify="center">
              <router-link to="/login"
                >Already have an account? Login</router-link
              >
            </v-row>
          </v-container>
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
  public email: string = "";
  public setPassword = false;
  public password1: string = "";
  public password2: string = "";
  public termsAccepted = false;

  public async submit() {
    if (await this.$validator.validateAll()) {
      const userProfile: IUserProfileCreate = {
        email: this.email,
        nickname: this.nickname,
      };
      userProfile.password = this.password1;
      const error = await dispatchCreateUser(this.$store, userProfile);
      if (!error) {
        this.$router.push("/profile");
      }
    }
  }
}
</script>

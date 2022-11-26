<template>
  <v-main>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title
                >Password Recovery</v-toolbar-title
              >
            </v-toolbar>
            <v-card-text>
              <p class="subheading">
                A password recovery email will be sent to the registered account
              </p>
              <v-form
                @keyup.enter="submit"
                v-model="valid"
                ref="form"
                @submit.prevent=""
                lazy-validation
              >
                <v-text-field
                  @keyup.enter="submit"
                  label="Email"
                  type="email"
                  prepend-icon="person"
                  v-model="email"
                  v-validate="'required|email'"
                  data-vv-delay="100"
                  data-vv-name="email"
                  :error-messages="errors.collect('email')"
                  required
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click="cancel">Cancel</v-btn>
              <v-btn @click.prevent="submit" :disabled="!valid">
                Recover Password
              </v-btn>
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
import { dispatchPasswordRecovery } from "@/store/main/actions";

@Component
export default class Login extends Vue {
  public valid = false;
  public email: string = "";
  public appName = appName;

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
    dispatchPasswordRecovery(this.$store, { email: this.email });
    }
  }
}
</script>

<style></style>

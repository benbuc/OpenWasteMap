<template>
  <v-card class="elevation-12">
    <v-card-text>
      <v-form @keyup.enter="submit">
        <v-text-field
          @keyup.enter="submit"
          v-model="email"
          prepend-icon="person"
          name="login"
          label="Login"
          type="text"
        ></v-text-field>
        <v-text-field
          @keyup.enter="submit"
          v-model="password"
          prepend-icon="lock"
          name="password"
          label="Password"
          id="password"
          type="password"
        ></v-text-field>
      </v-form>
      <div v-if="loginError">
        <v-alert :value="loginError" transition="fade-transition" type="error">
          Incorrect email or password
        </v-alert>
      </div>
      <v-flex class="caption text-xs-right"
        ><router-link to="/recover-password"
          >Forgot your password?</router-link
        ></v-flex
      >
      <v-flex class="caption text-xs-right">
        <router-link to="/signup">Signup new account</router-link>
      </v-flex>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn @click.prevent="submit">Login</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { api } from "@/api";
import { appName } from "@/env";
import { readIsLoggedIn, readLoginError } from "@/store/main/getters";
import { dispatchCheckLoggedIn, dispatchLogIn } from "@/store/main/actions";
import store from "@/store";

const routeGuardMain = async (to, from, next) => {
  await dispatchCheckLoggedIn(store);
  if (readIsLoggedIn(store)) {
    next("/");
  } else {
    next();
  }
};

@Component
export default class Login extends Vue {
  public email: string = "";
  public password: string = "";
  public appName = appName;

  public beforeRouteEnter(to, from, next) {
    routeGuardMain(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    routeGuardMain(to, from, next);
  }

  public get loginError() {
    return readLoginError(this.$store);
  }

  public submit() {
    dispatchLogIn(this.$store, {
      username: this.email,
      password: this.password,
    });
  }
}
</script>

<style></style>

<template>
  <v-main> </v-main>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
import { IUserProfileUpdate } from "@/interfaces";
import { appName } from "@/env";
import { commitAddNotification } from "@/store/main/mutations";
import { dispatchVerifyEmail } from "@/store/main/actions";

@Component
export default class UserProfileEdit extends Vue {
  public appName = appName;

  public async mounted() {
    const token = this.checkToken();
    if (token) {
      await dispatchVerifyEmail(this.$store, {
        token,
      });
      this.$router.push("/profile");
    }
  }

  public checkToken() {
    const token = this.$router.currentRoute.query.token as string;
    if (!token) {
      commitAddNotification(this.$store, {
        content: "No token provided. Please request a new verification e-mail",
        color: "error",
      });
      this.$router.push("/");
    } else {
      return token;
    }
  }
}
</script>

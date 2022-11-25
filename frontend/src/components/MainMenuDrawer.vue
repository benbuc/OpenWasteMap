<template>
  <v-navigation-drawer v-model="showDrawer" app temporary>
    <v-list-item class="px-2">
      <v-list-item-content v-if="userProfile">
        <v-list-item-title class="text-h6">
          Hi, {{ userProfile.nickname }}
        </v-list-item-title>
        <v-list-item-subtitle>{{ userProfile.email }}</v-list-item-subtitle>
      </v-list-item-content>
      <v-list-item-content v-else>
        <v-list-item-title class="text-h6">OpenWasteMap</v-list-item-title>
      </v-list-item-content>

      <v-list-item-action>
        <v-btn icon @click="showDrawer = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>

    <v-divider></v-divider>

    <v-list dense nav>
      <v-list-item-group>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          link
          @click="showDrawer = false"
          :to="item.link"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>

    <template v-slot:append>
      <div class="pa-2">
        <v-btn block @click="logout" v-if="userProfile">
          <v-icon left>mdi-logout</v-icon>
          Logout
        </v-btn>
        <v-btn block to="/login" v-else>
          <v-icon left>mdi-login</v-icon>
          Login
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { dispatchUserLogOut } from "@/store/main/actions";
import { readUserProfile } from "@/store/main/getters";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class MainMenuDrawer extends Vue {
  @Prop({ default: false }) value!: boolean;
  get showDrawer() {
    return this.value;
  }
  set showDrawer(value: boolean) {
    this.$emit("input", value);
  }
  get items() {
    return [
      {
        title: "Home",
        icon: "mdi-map",
        link: "/",
      },
      this.userProfile
        ? {
            title: "Profile",
            icon: "mdi-account",
            link: "/profile",
          }
        : {
            title: "Create Account",
            icon: "mdi-account-plus",
            link: "/signup",
          },
    ];
  }

  get userProfile() {
    return readUserProfile(this.$store);
  }
  async logout() {
    await dispatchUserLogOut(this.$store);
    this.showDrawer = false;
  }
}
</script>

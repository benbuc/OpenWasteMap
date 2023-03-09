<template>
  <div id="app">
    <v-app>
      <v-app-bar height="56px" app>
        <v-app-bar-nav-icon
          @click="showDrawer = true"
          v-if="$vuetify.breakpoint.smAndDown"
        ></v-app-bar-nav-icon>
        <v-app-bar-title to="/"> OpenWasteMap </v-app-bar-title>
        <v-spacer></v-spacer>
        <div v-if="$vuetify.breakpoint.mdAndUp">
          <v-btn
            v-for="(item, i) in menuItemsAppBar"
            :key="i"
            text
            :to="item.link"
            @click="item.click"
            class="ms-2"
          >
            <v-icon left>{{ item.icon }}</v-icon>
            {{ item.title }}
          </v-btn>
        </div>
      </v-app-bar>
      <MainMenuDrawer
        v-model="showDrawer"
        v-if="$vuetify.breakpoint.smAndDown"
        :items="menuItemsDrawer"
        :userProfile="userProfile"
      ></MainMenuDrawer>
      <NotificationsManager></NotificationsManager>
      <router-view></router-view>
    </v-app>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import NotificationsManager from "@/components/NotificationsManager.vue";
import MainMenuDrawer from "@/components/MainMenuDrawer.vue";
import { readUserProfile } from "./store/main/getters";
import { dispatchUserLogOut } from "./store/main/actions";

@Component({
  components: {
    NotificationsManager,
    MainMenuDrawer,
  },
})
export default class App extends Vue {
  showDrawer = false;

  public mounted() {
    document.body.style.overflow = "hidden";
    window.addEventListener("resize", this.onResize);
  }
  public unmounted() {
    window.removeEventListener("resize", this.onResize);
  }
  onResize() {
    document.body.style.height = window.innerHeight + "px";
  }

  get menuItemsDrawer() {
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
  get menuItemsAppBar() {
    if (this.userProfile) {
      return [
        {
          title: "Home",
          icon: "mdi-map",
          link: "/",
        },
        {
          title: "Profile",
          icon: "mdi-account",
          link: "/profile",
        },
        {
          title: "Logout",
          icon: "mdi-logout",
          click: this.logout,
        },
      ];
    } else {
      return [
        {
          title: "Login",
          icon: "mdi-login",
          link: "/login",
        },
        {
          title: "Signup",
          icon: "mdi-account-plus",
          link: "/signup",
        },
      ];
    }
  }
  get userProfile() {
    return readUserProfile(this.$store);
  }
  async logout() {
    await dispatchUserLogOut(this.$store);
    this.$router.push("/");
  }
}
</script>

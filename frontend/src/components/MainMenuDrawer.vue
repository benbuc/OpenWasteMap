<template>
  <v-navigation-drawer v-model="value" @input="handleInput" app>
    <v-list-item class="px-2">
      <v-list-item-avatar>
        <v-img src="@/assets/logo.png"></v-img>
      </v-list-item-avatar>

      <v-list-item-title>Hallo Welt</v-list-item-title>
    </v-list-item>

    <v-divider></v-divider>

    <v-list dense nav>
      <v-list-item-group>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          link
          @click="value = false"
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
        <v-btn block>
          <v-icon left>mdi-account</v-icon>
          Login
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class MainMenuDrawer extends Vue {
  @Prop({ default: false }) value!: boolean;
  handleInput() {
    this.$emit("input", this.value);
  }

  items = [
    { title: "Home", icon: "mdi-home" },
    { title: "About", icon: "mdi-account" },
    { title: "Contact", icon: "mdi-email" },
  ];
}
</script>

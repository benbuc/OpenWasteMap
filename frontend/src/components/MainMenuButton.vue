<template>
  <v-btn app fixed top left fab dark @click="showDrawer = !showDrawer">
    <v-icon>menu</v-icon>
  </v-btn>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class MainMenuButton extends Vue {
  @Prop({ default: false }) value!: boolean;
  get showDrawer() {
    return this.value;
  }
  set showDrawer(value: boolean) {
    this.$emit("input", value);
  }
}
</script>

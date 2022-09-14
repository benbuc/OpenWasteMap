<template>
  <v-speed-dial id="create-sample" v-model="active">
    <template v-slot:activator>
      <v-btn fab :style="{ transform: `rotate(${active ? 45 : 0}deg)` }">
        <v-icon>add</v-icon>
      </v-btn>
    </template>
    <v-tooltip v-model="showGPSTooltip" right v-if="showGPSWaiting">
      <template v-slot:activator="{ on }">
        <v-btn fab disabled loading v-on="on"> </v-btn
      ></template>
      <span
        >Waiting for GPS...{{
          coordinates.accuracy ? coordinates.accuracy.toFixed(2) : ""
        }}m</span
      >
    </v-tooltip>

    <v-btn
      fab
      :disabled="createButtonsDisabled"
      :style="{
        color: buttonColor(i - 1),
        border: `1px solid ${buttonColor(i - 1)}`,
      }"
      v-for="i in showCreateButtons ? 11 : 0"
      :key="i - 1"
      v-on:click="createSample(i - 1)"
      >{{ i - 1 }}</v-btn
    >
  </v-speed-dial>
</template>

<script lang="ts">
import { IWasteSampleCreate } from "@/interfaces";
import { dispatchCreateWasteSample } from "@/store/main/actions";
import { Vue, Component, Watch } from "vue-property-decorator";

@Component
export default class FABCreateSample extends Vue {
  public colors = [
    [0.0, 0.0, 255.0, 0.0],
    [0.2, 255.0, 248.0, 0.0],
    [0.3, 255.0, 171.0, 0.0],
    [0.75, 255.0, 0.0, 0.0],
    [0.9, 255.0, 13.0, 111.0],
    [1.0, 166.0, 150.0, 255.0],
  ];
  public active = false;
  public showCreateButtons = false;
  public createButtonsDisabled = false;
  public showGPSWaiting = true;
  public showGPSTooltip = false;
  public async mounted() {
    // prevent buttons from automatically closing the speed dial
    this.$el
      .querySelector(".v-speed-dial__list")!
      .addEventListener("click", (e) => {
        e.stopPropagation();
      });
    if (this.gpsReady) {
      this.showCreateButtons = true;
      this.showGPSWaiting = false;
      this.showGPSTooltip = false;
    }
  }
  @Watch("gpsReady")
  public gpsStatusChanged() {
    // to prevent objects from jumping on the screen we have to wait
    // for the old ones to disappear before we can add the new button
    // that's why if the gps status changes, we have to use timeouts
    // to exchange the button set
    // also, the tooltip has to be added when the button has layouted
    // therefore we wait for the animation to finish
    if (this.gpsReady) {
      // on ready, first remove the waiting notice and then add creation buttons
      this.showGPSWaiting = false;
      this.showGPSTooltip = false;
      setTimeout(() => {
        this.showCreateButtons = true;
      }, 250);
    } else {
      this.showCreateButtons = false;
      this.showGPSTooltip = false;
      setTimeout(() => {
        this.showGPSWaiting = true;
        setTimeout(() => {
          this.showGPSTooltip = true;
        }, 250);
      }, 250);
    }
  }
  @Watch("active")
  public activeChanged() {
    // see gpsStatusChanged for further information
    if (!this.active) {
      this.$vuexGeolocation.clearWatch();
      return;
    }
    this.$vuexGeolocation.watchPosition();
    if (!this.gpsReady) {
      this.showGPSTooltip = false;
      setTimeout(() => {
        this.showGPSTooltip = true;
      }, 250);
    }
  }
  get gpsReady() {
    return this.$store.state.geolocation.lat && this.coordinates.accuracy < 10;
  }
  get coordinates() {
    return {
      latitude: this.$store.state.geolocation.lat,
      longitude: this.$store.state.geolocation.lng,
      accuracy: this.$store.state.geolocation.acc,
    };
  }
  public buttonColor(wasteLevel: number) {
    let r = 0;
    let g = 0;
    let b = 0;
    for (let i = 0; i < this.colors.length - 1; i++) {
      if (
        wasteLevel / 10 >= this.colors[i][0] &&
        wasteLevel / 10 <= this.colors[i + 1][0]
      ) {
        const mix =
          (wasteLevel / 10 - this.colors[i][0]) /
          (this.colors[i + 1][0] - this.colors[i][0]);

        r = this.colors[i][1] * (1 - mix) + this.colors[i + 1][1] * mix;
        g = this.colors[i][2] * (1 - mix) + this.colors[i + 1][2] * mix;
        b = this.colors[i][3] * (1 - mix) + this.colors[i + 1][3] * mix;
      }
    }
    return `rgba(${r}, ${g}, ${b}, 1)`;
  }
  public async createSample(wasteLevel: number) {
    if (this.gpsReady) {
      this.createButtonsDisabled = true;
      const newSample: IWasteSampleCreate = {
        waste_level: wasteLevel,
        latitude: this.coordinates.latitude,
        longitude: this.coordinates.longitude,
      };
      await dispatchCreateWasteSample(this.$store, newSample);
      this.createButtonsDisabled = false;
      this.$root.$emit("refresh_owm_map");
      this.active = false;
    }
  }
}
</script>

<style>
#create-sample {
  position: fixed;
  bottom: 15px;
  left: 15px;
}
#create-sample .v-speed-dial__list .v-btn {
  margin: 0;
}
#create-sample .v-speed-dial__list .theme--dark.v-btn.v-btn--disabled {
  background: #373737 !important;
}
</style>

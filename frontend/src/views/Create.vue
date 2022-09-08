<template>
  <v-container>
    <v-row>
      <v-col class="text-right">
        <v-btn
          fab
          block
          v-for="i in 11"
          :style="{
            color: buttonStyle(i - 1),
            border: '1px solid ' + buttonStyle(i - 1),
          }"
          :key="i - 1"
          :disabled="!gpsReady"
          v-on:click="submit(i - 1)"
          >{{ i - 1 }}</v-btn
        >
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { IWasteSampleCreate } from "@/interfaces";
import { dispatchCreateWasteSample } from "@/store/main/actions";
import { Component, Vue } from "vue-property-decorator";

@Component
export default class Create extends Vue {
  public colors = [
    [0.0, 0.0, 255.0, 0.0],
    [0.2, 255.0, 248.0, 0.0],
    [0.3, 255.0, 171.0, 0.0],
    [0.75, 255.0, 0.0, 0.0],
    [0.9, 255.0, 13.0, 111.0],
    [1.0, 166.0, 150.0, 255.0],
  ];
  public valid = false;
  public wasteLevel: number = 0;
  public async mounted() {
    this.$vuexGeolocation.watchPosition();
  }
  get gpsReady() {
    return this.$store.state.geolocation.lat && this.coordinates.accuracy < 200;
  }
  get coordinates() {
    return {
      latitude: this.$store.state.geolocation.lat,
      longitude: this.$store.state.geolocation.lng,
      accuracy: this.$store.state.geolocation.acc,
    };
  }
  public buttonStyle(wasteLevel: number) {
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

  public async submit(wasteLevel: number) {
    if (this.gpsReady) {
      const newSample: IWasteSampleCreate = {
        waste_level: wasteLevel,
        latitude: this.coordinates.latitude,
        longitude: this.coordinates.longitude,
      };
      await dispatchCreateWasteSample(this.$store, newSample);
      this.$router.push("/");
    }
  }
}
</script>

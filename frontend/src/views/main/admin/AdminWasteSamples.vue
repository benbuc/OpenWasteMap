<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title> Manage Waste Samples </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" v-on:click="exportWasteSamplesPressed"
        >Export All</v-btn
      >
      <v-btn color="primary" to="/admin/waste-samples/create-bulk"
        >Bulk Import</v-btn
      >
    </v-toolbar>
    <v-data-table :headers="headers" :items="waste_samples">
      <template v-slot:body="{ items }">
        <tbody>
          <tr v-for="item in items" :key="item.name">
            <td>{{ item.waste_level }}</td>
            <td>{{ item.latitude.toFixed(5) }}</td>
            <td>{{ item.longitude.toFixed(5) }}</td>
            <td>{{ item.sampling_date | formatDate }}</td>
          </tr>
        </tbody>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { readAdminWasteSamples } from "@/store/admin/getters";
import {
  dispatchExportAllWasteSamples,
  dispatchGetWasteSamples,
} from "@/store/admin/actions";

@Component
export default class AdminWasteSamples extends Vue {
  public headers = [
    {
      text: "Waste Level",
      sortable: true,
      value: "waste_level",
      align: "left",
    },
    {
      text: "Latitude",
      sortable: true,
      value: "latitude",
      align: "left",
    },
    {
      text: "Longitude",
      sortable: true,
      value: "longitude",
      align: "left",
    },
    {
      text: "Sampling Date",
      sortable: true,
      value: "sampling_date",
      align: "left",
    },
  ];
  get waste_samples() {
    return readAdminWasteSamples(this.$store);
  }

  public async mounted() {
    await dispatchGetWasteSamples(this.$store);
  }

  public async exportWasteSamplesPressed() {
    await dispatchExportAllWasteSamples(this.$store);
  }
}
</script>

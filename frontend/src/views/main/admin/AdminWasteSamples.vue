<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title>
        Manage Waste Samples
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/admin/main/admin/waste-samples/create">Create Waste Sample</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="waste_samples">
      <template slot="items" slot-scope="props">
        <td>{{ props.item.waste_level }}</td>
        <td>{{ props.item.latitude.toFixed(5) }}</td>
        <td>{{ props.item.longitude.toFixed(5) }}</td>
        <td class="justify-center layout px-0">
          <v-tooltip top>
            <span>Edit</span>
            <v-btn slot="activator" flat :to="{name: 'main-admin-waste-samples-edit', params: {id: props.item.id}}">
              <v-icon>edit</v-icon>
            </v-btn>
          </v-tooltip>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { IUserProfile } from '@/interfaces';
import { readAdminWasteSamples } from '@/store/admin/getters';
import { dispatchGetWasteSamples } from '@/store/admin/actions';

@Component
export default class AdminWasteSamples extends Vue {
  public headers = [
    {
      text: 'Waste Level',
      sortable: true,
      value: 'waste_level',
      align: 'left',
    },
    {
      text: 'Latitude',
      sortable: true,
      value: 'latitude',
      align: 'left',
    },
    {
      text: 'Longitude',
      sortable: true,
      value: 'longitude',
      align: 'left',
    },
    {
      text: 'Actions',
      value: 'id',
    },
  ];
  get waste_samples() {
    return readAdminWasteSamples(this.$store);
  }

  public async mounted() {
    await dispatchGetWasteSamples(this.$store);
  }
}
</script>

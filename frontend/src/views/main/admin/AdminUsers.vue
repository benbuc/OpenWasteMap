<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title> Manage Users </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" v-on:click="exportButtonClicked">Export All</v-btn>
      <v-btn color="primary" to="/admin/users/create">Create User</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="users">
      <template v-slot:body="{ items }">
        <tbody>
          <tr v-for="item in items" :key="item.name">
            <td>{{ item.nickname }}</td>
            <td>{{ item.email }}</td>
            <td><v-icon v-if="item.is_active">checkmark</v-icon></td>
            <td><v-icon v-if="item.is_superuser">checkmark</v-icon></td>
            <td>
              <v-btn
                text
                :to="{ name: 'main-admin-users-edit', params: { id: item.id } }"
              >
                <v-icon>edit</v-icon>
              </v-btn>
            </td>
          </tr>
        </tbody>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";
import { IUserProfile } from "@/interfaces";
import { readAdminUsers } from "@/store/admin/getters";
import {
  dispatchExportAllUsers,
  dispatchGetUsers,
} from "@/store/admin/actions";

@Component
export default class AdminUsers extends Vue {
  public headers = [
    {
      text: "Nickname",
      sortable: true,
      value: "nickname",
      align: "left",
    },
    {
      text: "Email",
      sortable: true,
      value: "email",
      align: "left",
    },
    {
      text: "Is Active",
      sortable: true,
      value: "isActive",
      align: "left",
    },
    {
      text: "Is Superuser",
      sortable: true,
      value: "isSuperuser",
      align: "left",
    },
    {
      text: "Actions",
      value: "id",
    },
  ];
  get users() {
    return readAdminUsers(this.$store);
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
  }

  public async exportButtonClicked() {
    await dispatchExportAllUsers(this.$store);
  }
}
</script>

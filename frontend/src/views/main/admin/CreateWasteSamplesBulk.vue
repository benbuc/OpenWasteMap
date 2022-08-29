<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Bulk Import Waste Samples</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-textarea
              outlined
              name="input-json"
              label="Paste JSON"
              v-model="inputJSON"
              @change="jsonUpdated"
              required
            ></v-textarea>
          </v-form>
        </template>
        <p>{{ statusMessage }}</p>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="submit" :disabled="!valid">
              Import
            </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
  IWasteSampleCreateBulk,
} from '@/interfaces';
import { dispatchGetUsers, dispatchCreateUser, dispatchCreateWasteSamplesBulk } from '@/store/admin/actions';

@Component
export default class CreateUser extends Vue {
  public valid = false;
  public inputJSON: string = '';
  public statusMessage: string = 'No Content';
  public processedJSON: IWasteSampleCreateBulk[] = [];

  public jsonUpdated(event: InputEvent) {
    let obj = JSON.parse(this.inputJSON) as IWasteSampleCreateBulk[];
    this.statusMessage = "Found " + obj.length + " objects";
    this.processedJSON = obj;
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
    this.reset();
  }

  public reset() {
    this.inputJSON = '';
    this.$validator.reset();
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      await dispatchCreateWasteSamplesBulk(this.$store, this.processedJSON);
      this.$router.push('/admin/main/admin/waste-samples');
    }
  }
}
</script>

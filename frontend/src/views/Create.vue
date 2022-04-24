<template>
    <v-card class="elevation-12">
        <v-card-text>
            <v-form v-model="valid" ref="form">
                {{ coordinates.latitude }} - 
                {{ coordinates.longitude }} - 
                {{ coordinates.accuracy }}
                <input type="hidden" id="latitude" v-model="coordinates.latitude">
                <input type="hidden" id="longitude" v-model="coordinates.longitude">
                <v-text-field label="Waste Level"  v-model="wasteLevel" required></v-text-field>
            </v-form>
        </v-card-text>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="submit" :disabled="!valid || !gpsReady">
                Save
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script lang="ts">
import { IWasteSampleCreate } from '@/interfaces';
import { dispatchCreateWasteSample } from '@/store/main/actions';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Create extends Vue {
    public valid = false;
    public wasteLevel: number = 0;
    public async mounted() {
        this.$vuexGeolocation.watchPosition();
    }
    get gpsReady() {
        return this.coordinates.accuracy < 200;
    }
    get coordinates() {
        return {
            latitude: this.$store.state.geolocation.lat,
            longitude: this.$store.state.geolocation.lng,
            accuracy: this.$store.state.geolocation.acc,
        };
    }

    public async submit() {
        if (this.gpsReady) {
            const newSample: IWasteSampleCreate = {
                waste_level: this.wasteLevel,
                latitude: this.coordinates.latitude,
                longitude: this.coordinates.longitude,
            };
            await dispatchCreateWasteSample(this.$store, newSample);
            this.$router.push('/');
        }
    }
}
</script>
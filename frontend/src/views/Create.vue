<template>
    <v-card class="elevation-12" :style="cardStyle">
        <v-card-text>
            <v-form v-model="valid" ref="form"> 
                Position accuracy: {{ coordinates.accuracy }} m
                <v-slider min="0" max="10" label="Waste Level" v-model="wasteLevel"></v-slider>
                Level: {{ wasteLevel }}
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
    colors = [
        [0.0, 0.0, 255.0, 0.0],
        [0.2, 255.0, 248.0, 0.0],
        [0.30, 255.0, 171.0, 0.0],
        [0.75, 255.0, 0.0, 0.0],
        [0.9, 255.0, 13.0, 111.0],
        [1.0, 166.0, 150.0, 255.0],
    ]
    public valid = false;
    public wasteLevel: number = 0;
    public async mounted() {
        this.$vuexGeolocation.watchPosition();
    }
    get gpsReady() {
        return this.$store.state.geolocation.lat && (this.coordinates.accuracy < 200);
    }
    get coordinates() {
        return {
            latitude: this.$store.state.geolocation.lat,
            longitude: this.$store.state.geolocation.lng,
            accuracy: this.$store.state.geolocation.acc,
        };
    }
    get cardStyle() {
        var r = 0;
        var g = 0;
        var b = 0;
        for (let i=0; i<this.colors.length-1; i++) {
            if ((this.wasteLevel / 10 >= this.colors[i][0]) && (this.wasteLevel / 10 <= this.colors[i+1][0])) {
                const mix = ((this.wasteLevel / 10) - this.colors[i][0]) / (this.colors[i+1][0] - this.colors[i][0]);

                r = (this.colors[i][1] * (1 - mix) + this.colors[i+1][1] * mix);
                g = (this.colors[i][2] * (1 - mix) + this.colors[i+1][2] * mix);
                b = (this.colors[i][3] * (1 - mix) + this.colors[i+1][3] * mix);
            }
        }
        return `background: rgba(${r}, ${g}, ${b}, 1)`;
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
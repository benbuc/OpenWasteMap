<template>
    <v-card class="elevation-12">
        <v-card-text>
            <v-form>
                <input type="hidden" id="latitude" v-model="latitude">
                <input type="hidden" id="longitude" v-model="longitude">
                
                <template v-if="location">{{ location.coords.latitude }}, {{ location.coords.longitude }}</template>
                <template v-if="errorStr">{{ errorStr }}</template>
                <template v-if="gettingLocation">Getting Location...</template>
            </v-form>
        </v-card-text>
    </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Create extends Vue {
    errorStr = '';
    gettingLocation = false;
    location?: GeolocationPosition;
    public async mounted() {
        if (!("geolocation" in navigator)) {
            this.errorStr = 'Geolocation is not available.';
            return
        }

        this.gettingLocation = true;
        navigator.geolocation.getCurrentPosition(pos => {
            this.gettingLocation = false;
            this.location = pos;
        })
    }
}
</script>
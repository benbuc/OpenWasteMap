import Vue from 'vue';
import VuexGeolocation from 'vuex-geolocation';

// Compilation failed because $vuexGeolocation could not be found for this
// in the components. This installs the correct type.
declare module 'vue/types/vue' {
    interface Vue {
        $vuexGeolocation: VuexGeolocation;
    }
}

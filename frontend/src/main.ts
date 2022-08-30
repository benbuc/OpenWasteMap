import '@babel/polyfill';
// Import Component hooks before component definitions
import './component-hooks';
import Vue from 'vue';
import './plugins/vuetify';
import './plugins/vee-validate';
import App from './App.vue';
import router from './router';
import store from '@/store';
import './registerServiceWorker';
import 'vuetify/dist/vuetify.min.css';
import L from 'leaflet';
import { LMap, LTileLayer, LMarker } from 'vue2-leaflet';
import 'leaflet/dist/leaflet.css';
import { Icon } from 'leaflet';
import VuexGeolocation from 'vuex-geolocation';
import moment from 'moment';

// Compilation failed because $vuexGeolocation could not be found for this
// in the components. This installs the correct type.
declare module 'vue/types/vue' {
  interface Vue {
    $vuexGeolocation: VuexGeolocation;
  }
}

Vue.component('l-map', LMap);
Vue.component('l-tile-layer', LTileLayer);
Vue.component('l-marker', LMarker);
Vue.filter('formatDate', function (value: string) {
  if (value) {
    return moment(String(value)).format('YYYY-MM-DD HH:mm');
  }
});

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');

// Marker Icons missing for leaflet
// https://vue2-leaflet.netlify.app/quickstart/#marker-icons-are-missing

type D = Icon.Default & {
  _getIconUrl?: string;
};

delete (Icon.Default.prototype as D)._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';
import VuexGeolocation from 'vuex-geolocation';

import { mainModule } from './main';
import { State } from './state';
import { adminModule } from './admin';

Vue.use(Vuex);

const storeOptions: StoreOptions<State> = {
  modules: {
    main: mainModule,
    admin: adminModule,
  },
};

export const store = new Vuex.Store<State>(storeOptions);

const vuexGeolocation = VuexGeolocation.sync(store, { autoWatch: false });
Vue.use(vuexGeolocation);

export default store;

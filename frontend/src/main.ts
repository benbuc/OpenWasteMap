// Import Component hooks before component definitions
import "./component-hooks";
import Vue from "vue";
import "./plugins/vee-validate";
import "./plugins/leaflet";
import "./plugins/vuex-geolocation";
import "./plugins/moment";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import router from "./router/routes";
import store from "@/store";
import "./registerServiceWorker";
import "vuetify/dist/vuetify.min.css";
import "material-design-icons-iconfont/dist/material-design-icons.css";
import "@mdi/font/css/materialdesignicons.css";

Vue.config.productionTip = false;

new Vue({
  vuetify,
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");

<template>
  <v-main>
    <OwmMap />

    <v-dialog v-model="showDialog" width="500">
      <router-view></router-view>
    </v-dialog>

    <FABCreateSample></FABCreateSample>
  </v-main>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import OwmMap from "../components/OwmMap.vue";
import FABCreateSample from "../components/FABCreateSample.vue";
import { dispatchCheckLoggedIn } from "@/store/main/actions";

@Component({
  components: {
    OwmMap,
    FABCreateSample,
  },
})
export default class Home extends Vue {
  public get showDialog() {
    return this.$route.name !== "home";
  }
  public set showDialog(value: boolean) {
    if (!value) {
      this.$router.push({ name: "home" });
    }
  }
  public async mounted() {
    dispatchCheckLoggedIn(this.$store);
  }
}
</script>

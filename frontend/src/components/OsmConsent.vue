<template>
    <div class="osm-consent">
        <div class="osm-consent__content">
        <h2 class="osm-consent__title">OpenStreetMap</h2>
        <p class="osm-consent__text">
            We use OpenStreetMap as the background map. By using this map you agree to the
            <a
            href="https://wiki.osmfoundation.org/wiki/Privacy_Policy"
            target="_blank"
            rel="noopener noreferrer"
            >OpenStreetMap privacy policy</a
            >.
        </p>
        <div class="osm-consent__buttons">
            <button
            class="osm-consent__button osm-consent__button--accept"
            @click="accept"
            >
            Accept
            </button>
            <button
            class="osm-consent__button osm-consent__button--decline"
            @click="decline"
            >
            Decline
            </button>
        </div>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class OsmConsent extends Vue {
  public accept() {
    localStorage.setItem("osmConsent", "true");
    this.$root.$emit("update_osm_consent");
  }
  public decline() {
    localStorage.setItem("osmConsent", "false");
    this.$root.$emit("update_osm_consent");
  }
}
</script>

<style scoped>
.osm-consent {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  color: black;    
}
.osm-consent_buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}
.osm-consent__button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  font-size: 1rem;
  cursor: pointer;
}
.osm-consent__content {
  background-color: white;
  padding: 1rem;
  border-radius: 0.25rem;
  min-width: 300px;
}
.osm-consent__title {
  font-size: 1.5rem;
}
.osm-consent__button--accept {
  background-color: #4caf50;
  color: white;
}
.osm-consent__button--decline {
  background-color: #f44336;
  color: white;
}
</style>
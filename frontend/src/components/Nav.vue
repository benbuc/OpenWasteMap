<template>
    <div class="menu-wrapper">
        <v-btn class="mx-2" fab color="primary" to="/login">
            <v-icon>
                person
            </v-icon>
        </v-btn>
    </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

@Component
export default class Nav extends Vue {

}

</script>

<style scoped>
.menu-wrapper {
    position: fixed;
    top: 15px;
    right: 15px;
}
</style>
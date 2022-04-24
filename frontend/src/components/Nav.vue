<template>
    <div class="buttons-wrapper">
        <v-btn v-if="loggedIn" class="mx-2" fab>
            <v-icon>
                add                
            </v-icon>
        </v-btn>
        <v-btn class="mx-2" fab dark :color="buttonColor" :to="buttonLink">
            <v-icon>
                person
            </v-icon>
        </v-btn>
    </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import { readIsLoggedIn } from '@/store/main/getters';

@Component
export default class Nav extends Vue {
    public get buttonLink() {
        return (this.$route.path !== '/login') ? '/login' : '/';
    }
    public get buttonColor() {
        if (readIsLoggedIn(this.$store)) {
            return 'green';
        }
        if (this.$route.path === '/login') {
            return 'primary';
        }
        return 'grey';
    }
    get loggedIn() {
        return readIsLoggedIn(this.$store);
    }
}
</script>

<style scoped>
.buttons-wrapper {
    text-align: right;
    margin-bottom: 10px;
}
</style>
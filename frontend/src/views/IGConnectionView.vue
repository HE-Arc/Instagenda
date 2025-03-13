<template>
</template>

<style>
@media (min-width: 1024px) {
.about {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
}
</style>

<script setup>
import axios from 'axios';
import { onMounted } from 'vue';
import router from '@/router'
import { useRoute } from 'vue-router';

const route = useRoute();
const code = route.query.code;

console.log(code)

async function postCode() {
    const response = await axios.post('/ig/connection/', { code: code })
    return response.data
}

onMounted(async () => {
    await postCode()
    // redirect to the user view
    router.push('/user')
})
</script>
  
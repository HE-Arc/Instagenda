<script setup>
import { ref, onMounted } from 'vue'
import { QBtn } from 'quasar'
import router from '@/router'
import axios from 'axios'

const profile = ref('')

async function getProfile() {
    const response = await axios.get('/profile/')
    return response.data
}

onMounted(async () => {
    profile.value = await getProfile()
})

async function logout() {
    await axios.post('/logout/')
    profile.value = ''
    router.push('/')
}
</script>

<template>
    <div class="user">
        <h2>username : {{profile.username}}</h2>
    </div>
</template>

<style>
@media (min-width: 1024px) {
  .user {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
}
</style>

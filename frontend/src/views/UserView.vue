<script setup>
import { ref, onMounted } from 'vue'
import { QBtn } from 'quasar'
import router from '@/router'
import axios from 'axios'

const profile = ref('')

async function getProfile() {
    const response = await axios.get('/profile')
    return response.data
}

onMounted(async () => {
    profile.value = await getProfile()
})

async function logout() {
    await axios.post('/logout')
    profile.value = ''
    router.push('/')
}
</script>

<template>
    <div class="user">
        <h1>This is when you are logged</h1>
        <h2>profile : {{profile}}</h2>
        <QBtn label="Logout" @click="logout"/>
    </div>
</template>
  
<style>
@media (min-width: 1024px) {
  .user {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
  
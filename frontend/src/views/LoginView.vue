<script setup>
import { ref, onMounted } from 'vue'
import { QInput, QBtn } from 'quasar'
import axios from 'axios'
import router from '@/router'
import { updateCSRF } from '@/main'

const username = ref('')
const password = ref('')

const status = ref('')

const login = async () => {
  try {
    await axios.post('/login', {
      username: username.value,
      password: password.value
    })
    updateCSRF()
    router.push('/')
  } catch (error) {
    console.error(error)
  }
}

const register = async () => {
  router.push('/register')
}

onMounted(async () => {
  try {
    const response = await axios.get('/backend-status')
    status.value = response.data.status
  } catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <main>
    <h1>Backend status: {{status}}</h1>
    <h1>Login</h1>

    <QInput v-model="username" label="Username"/>
    <QInput v-model="password" label="Password" type="password"/>
    <QBtn label="Login" @click="login"/>
    <QBtn label="Register" @click="register"/>
  </main>
</template>
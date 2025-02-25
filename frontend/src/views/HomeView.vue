<script setup>
import { ref, onMounted } from 'vue'
import { QInput, QBtn } from 'quasar'
import axios from 'axios'
import router from '@/router'
import { updateCSRF } from '@/main'

const username = ref('')
const password = ref('')
const username_register = ref('')
const password_register = ref('')

const status = ref('')

const login = async () => {
  try {
    await axios.post('/login', {
      username: username.value,
      password: password.value
    })
    updateCSRF()
    router.push('/user')
  } catch (error) {
    console.error(error)
  }
}

const register = async () => {
  try {
    await axios.post('/register', {
      username: username_register.value,
      password: password_register.value
    })
    updateCSRF()
    router.push('/user')
  } catch (error) {
    console.error(error)
  }
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

    <h1>Register</h1>
    <QInput v-model="username_register" label="Username"/>
    <QInput v-model="password_register" label="Password" type="password"/>
    <QBtn label="Register" @click="register"/>
  </main>
</template>
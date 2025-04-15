<script setup>
import { ref } from 'vue'
import { QInput, QBtn, QImg } from 'quasar'
import axios from 'axios'
import router from '@/router'
import { updateCSRF } from '@/main'
import { useErrorMessage } from '@/components/store'

const username = ref('')
const password = ref('')
const { errorMessage } = useErrorMessage()

const login = async () => {
  try {
    await axios.post('/login/', {
      username: username.value,
      password: password.value
    })
    updateCSRF()
    router.push('/')
  } catch (error) {
    errorMessage.value = 'Erreur lors de la connexion : ' + error.response?.data.error || error
  }
}

</script>

<template>
  <main>
    <div class="bg-white flex flex-center column container">
      <!-- Logo -->
      <QImg
        src="/assets/images/logo_slogan.png"
        class="logo"
        fit="contain"
      />

      <!-- Form -->
      <div class="form-container">
        <QInput v-model="username" label="Nom d'utilisateur" rounded outlined color="primary" class="q-mb-md"/>
        <QInput v-model="password" label="Mot de passe" type="password" rounded outlined color="primary" class="q-mb-md"/>

        <QBtn label="Se connecter" @click="login" class="full-width btn-login" color="primary" rounded/>
      </div>

      <!-- Register -->
      <div class="register-container">
        <p>Pas encore de compte ? <span class="register-text" @click="router.push('/register')">S'enregistrer</span></p>
      </div>
    </div>
  </main>
</template>

<style scoped>
.logo {
  width: 100%;
  max-width: 500px;
  height: auto;
  display: block;
  margin: 0vh auto 5vh;
}

.container {
  min-height: 100vh;
  padding-bottom: 10%;
}

.form-container {
  width: 100%;
  max-width: 450px;
  padding: 20px;
}

.register-container {
  width: 100%;
  text-align: center;
}

.register-text {
  cursor: pointer;
  color: #F5545B;
  text-decoration: underline;
}

</style>

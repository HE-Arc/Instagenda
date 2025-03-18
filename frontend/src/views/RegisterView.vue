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

const register = async () => {
  try {
    await axios.post('/register/', {
      username: username.value,
      password: password.value
    })
    updateCSRF()
    router.push('/')
  } catch (error) {
    errorMessage.value = 'Erreur lors de l\'enregistrement : ' + error.response?.data.error || error
  }
}
</script>

<template>
  <main>
    <div class="fullscreen bg-white flex flex-center column container">
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

        <QBtn label="S'enregistrer" @click="register" class="full-width btn-register" color="primary" rounded/>
      </div>

      <!-- Login -->
      <div class="login-container">
        <p>Déjà un compte ? <span class="login-text" @click="router.push('/login')">Se connecter</span></p>
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
  margin-bottom: 10vh;
}

.form-container {
  width: 100%;
  max-width: 450px;
  padding: 20px;
}

.login-container {
  width: 100%;
  text-align: center;
}

.login-text {
  cursor: pointer;
  color: #F5545B;
  text-decoration: underline;
}
</style>

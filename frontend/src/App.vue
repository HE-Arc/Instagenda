<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { QBtn, QImg } from 'quasar'
import axios from 'axios'
import router from '@/router'

async function logout() {
    await axios.post('/logout/')
    router.push('/login')
}
</script>

<template>
  <header>
    <div>
      <nav class="wrapper">
        <!-- Logo -->
        <RouterLink to="/" class="logo">
          <QImg src="/assets/images/logo.png" fit="contain" class="logo-img" />
        </RouterLink>

        <QBtn label="Déconnexion" color="primary" rounded @click="logout" class="logout-btn" />
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  width: 100%;
  padding: 1rem 2rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.wrapper {
  display: flex;
  align-items: center;
}

.logo-img {
  height: auto;
  width: 150px;
  display: block;
}

.logout-btn {
  font-size: 14px;
  padding: 6px 12px;
  margin-left: auto;
}
</style>

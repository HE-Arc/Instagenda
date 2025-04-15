<script setup>
import { useRoute } from 'vue-router'
import { RouterLink, RouterView } from 'vue-router'
import { QBtn, QImg } from 'quasar'
import axios from 'axios'
import router from '@/router'
import ErrorBanner from '@/components/ErrorBanner.vue'

const route = useRoute()

async function logout() {
  await axios.post('/logout/')
  router.push('/login')
}

const hideLayoutOnRoutes = ['/login', '/register']
</script>

<template>
  <header v-if="!hideLayoutOnRoutes.includes(route.path)" class="app-header">
    <nav class="wrapper">
      <RouterLink to="/" class="logo">
        <QImg src="/assets/images/logo.png" fit="contain" class="logo-img" />
      </RouterLink>

      <div class="nav-buttons">
        <QBtn icon="person" color="primary" rounded @click="router.push('/user')" />
        <QBtn icon="logout" color="primary" rounded @click="logout" />
      </div>
    </nav>
  </header>

  <ErrorBanner />

  <main class="app-main">
    <RouterView />
  </main>

  <footer class="app-footer" v-if="!hideLayoutOnRoutes.includes(route.path)">
    <QBtn to="/about" label="À propos" color="primary" flat class="about-btn" />
  </footer>
</template>

<style scoped lang="scss">
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 70px;
  background: $white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
  padding: 0 2rem;
}

.wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.logo-img {
  width: 150px;
  height: auto;
}

.nav-buttons {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 70px;
  background: $white;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* MAIN */
.app-main {
  padding: 20px;
  margin-top: 70px;
  margin-bottom: 70px;
}
</style>

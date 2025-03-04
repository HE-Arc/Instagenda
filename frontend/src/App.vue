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

        <div class="nav-buttons">
          <QBtn
            icon="person"
            color="primary"
            rounded
            @click="router.push('/user')"
            class="logout-btn"
          />

          <QBtn
            icon="logout"
            color="primary"
            rounded
            @click="logout"
            class="logout-btn"
          />
        </div>
      </nav>
    </div>
  </header>

  <RouterView />

  <!-- Footer Section with QBtn as the link -->
  <footer>
    <div class="footer-content">
      <QBtn
        to="/about"
        label="A propos"
        color="primary"
        flat
        class="about-btn"
      />
    </div>
  </footer>
</template>

<style scoped>
/* Make the header fixed at the top of the page */
header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  padding: 1rem 2rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-img {
  height: auto;
  width: 150px;
  display: block;
}

/* Align buttons to the right */
.nav-buttons {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.logout-btn {
  font-size: 14px;
  padding: 6px 12px;
  margin-left: 8px;
}

/* Make the footer fixed at the bottom of the page */
footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.footer-content {
  display: flex;
  justify-content: center;
}

/* Style for the About button */
.about-btn {
  font-weight: bold;
}

/* Main content area should take available space between header and footer */
main {
  padding: 4rem 2rem 4rem; /* Adds padding to the top and bottom to prevent overlap with fixed header/footer */
  min-height: calc(100vh - 8rem); /* Makes sure the content fills the space between header and footer */
  overflow-y: auto; /* Enable scrolling for content */
}
</style>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const profile = ref('')
const instagramAuthUrl = import.meta.env.VITE_INSTAGRAM_URL

async function getProfile() {
    const response = await axios.get('/profile/')
    return response.data
}

onMounted(async () => {
    profile.value = await getProfile()
})
</script>

<template>
    <div class="user">
      <div class="profile-content">
        <h2>Username: {{ profile.username }}</h2>
        <a :href="instagramAuthUrl" class="instagram-button">
          <img src="/assets/images/instagram.svg" alt="Instagram" class="instagram-icon" />
          Link with Instagram
        </a>
      </div>
    </div>
</template>

<style>
.user {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.profile-content {
  text-align: center;
}

.instagram-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #e1306c;
  color: white;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 8px;
  font-weight: bold;
  margin-top: 20px;
}

.instagram-icon {
  width: 24px;
  height: 24px;
}
</style>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { QBtn, QInput } from 'quasar'
import { useAuth } from '@/components/store'

const profile = ref('')
const instagramAuthUrl = import.meta.env.VITE_INSTAGRAM_URL

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const { user } = useAuth()

async function getProfile() {
  const response = await axios.get(`/users/${user.value.id}/`)
  return response.data
}

async function updateUsername() {
  const response = await axios.put(`/users/${user.value.id}/`, {
    username: profile.value.username
  })
  return response.data
}

onMounted(async () => {
  profile.value = await getProfile()
})

const saveProfile = () => {
  if (profile.value.username === '') {
    alert("Le nom d'utilisateur est requis")
    return
  }
  updateUsername()
    .then(() => {
      alert("Profil mis à jour avec succès")
    })
    .catch((error) => {
      console.error(error)
      alert("Erreur lors de la mise à jour du profil")
    })
}

const savePassword = () => {
  if (newPassword.value !== confirmPassword.value) {
    alert("Les mots de passe ne correspondent pas")
    return
  }

  axios.post('/users/change_password/', {
    current_password: currentPassword.value,
    new_password: newPassword.value,
    confirm_new_password: confirmPassword.value
  })
    .then(() => {
      alert("Mot de passe mis à jour avec succès")
      currentPassword.value = ''
      newPassword.value = ''
      confirmPassword.value = ''
    })
    .catch((error) => {
      console.error(error)
      alert("Erreur lors de la mise à jour du mot de passe")
    })
}
</script>

<template>
  <div class="main">
    <div class="card">
      <div class="card-header">
        <h3>Instagram account linked</h3>
      </div>
      <div class="card-body">
        <a :href="instagramAuthUrl" class="instagram-button">
          <img src="/assets/images/instagram.svg" alt="Instagram" class="instagram-icon" />
          Link with Instagram
        </a>
      </div>
    </div>

    <div class="card profile-card">
      <div class="card-header">
        <h3>Profile informations</h3>
      </div>
      <div class="card-body">
        <div class="input-group">
          <label for="username">Username</label>
          <QInput v-model="profile.username" id="username" label="Username" outlined />
        </div>
        <div class="save-button">
          <QBtn label="Save" color="primary" @click="saveProfile" />
        </div>
      </div>
    </div>

    <div class="card password-card">
      <div class="card-header">
        <h3>Modify password</h3>
      </div>
      <div class="card-body">
        <div class="input-group">
          <label for="current-password">Current Password</label>
          <QInput v-model="currentPassword" id="current-password" type="password" label="Current Password" outlined />
        </div>
        <div class="input-group">
          <label for="new-password">New Password</label>
          <QInput v-model="newPassword" id="new-password" type="password" label="New Password" outlined />
        </div>
        <div class="input-group">
          <label for="confirm-password">Confirm New Password</label>
          <QInput v-model="confirmPassword" id="confirm-password" type="password" label="Confirm New Password" outlined />
        </div>
        <div class="save-button">
          <QBtn label="Save Password" color="primary" @click="savePassword" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.card {
  width: 80%;
  background-color: #f1f1f1;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.card-header {
  background-color: #e0e0e0;
  padding: 15px;
  border-radius: 10px 10px 0 0;
}

.card-header h3 {
  margin: 0;
  font-size: 2rem;
}

.card-body {
  padding: 20px;
}

.instagram-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #e1306c;
  color: $white;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 8px;
  font-weight: bold;
}

.instagram-icon {
  width: 24px;
  height: 24px;
}

.profile-card {
  margin-top: 20px;
}

.password-card {
  margin-top: 20px;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.save-button {
  text-align: left;
}
</style>

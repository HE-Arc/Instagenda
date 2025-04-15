<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { QBtn, QInput, QSpinner } from 'quasar'
import { useAuth } from '@/components/store'

const { user } = useAuth()

const profile = ref('')
const instagramStatus = ref({ connected: false })
const instagramLoading = ref(true)
const instagramError = ref(null)
const currentPasswordRef = ref(null)
const newPasswordRef = ref(null)
const confirmPasswordRef = ref(null)

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const instagramAuthUrl = import.meta.env.VITE_INSTAGRAM_URL

async function getProfile() {
  const response = await axios.get(`/users/${user.value.id}/`, { withCredentials: true })
  return response.data
}

async function updateUsername() {
  const response = await axios.put(`/users/${user.value.id}/`, {
    username: profile.value.username
  }, { withCredentials: true })
  return response.data
}

async function fetchInstagramStatus() {
  try {
    const response = await axios.get('/ig/status/', { withCredentials: true })
    instagramStatus.value = response.data
  } catch (err) {
    instagramError.value = 'Erreur lors de la récupération du statut Instagram'
  } finally {
    instagramLoading.value = false
  }
}

async function disconnectInstagram() {
  try {
    await axios.delete('/ig/disconnect/', { withCredentials: true })
    await fetchInstagramStatus()
  } catch (err) {
    instagramError.value = 'Erreur lors de la déconnexion'
  }
}

onMounted(async () => {
  profile.value = await getProfile()
  await fetchInstagramStatus()
})

const saveProfile = () => {
  if (profile.value.username === '' || profile.value.username.length < 4 || profile.value.username.length > 50) {
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
  if (newPassword.value !== confirmPassword.value || !newPassword.value || !confirmPassword.value || newPassword.value.length < 6 || newPassword.value.length > 255) {
    return
  }

  axios.post('/users/change_password/', {
    current_password: currentPassword.value,
    new_password: newPassword.value,
    confirm_new_password: confirmPassword.value
  }, { withCredentials: true })
    .then(() => {
      alert("Mot de passe mis à jour avec succès")
      currentPassword.value = ''
      newPassword.value = ''
      confirmPassword.value = ''
      currentPasswordRef.value.resetValidation()
      newPasswordRef.value.resetValidation()
      confirmPasswordRef.value.resetValidation()
    })
    .catch((error) => {
      console.error(error)
      alert("Erreur lors de la mise à jour du mot de passe")
    })
}
const passwordMatchRule = (val) => val === newPassword.value || 'Les mots de passe doivent correspondre'
</script>

<template>
  <div class="main">
    <!-- COMPTE INSTAGRAM -->
    <div class="card">
      <div class="card-header">
        <h3>Compte Instagram</h3>
      </div>
      <div class="card-body">
        <div v-if="instagramLoading">
          <QSpinner color="primary" size="30px" />
        </div>

        <div v-else>
          <div v-if="instagramStatus.connected">
            <a :href="`https://instagram.com/${instagramStatus.username}`" target="_blank" class="ig-connected-link">
              <div class="ig-connected-box">
                <img src="/assets/images/instagram.svg" alt="Instagram" class="ig-connected-icon" />
                <div>
                  <p class="ig-connected-text">Connecté à Instagram</p>
                  <p class="ig-connected-user">@{{ instagramStatus.username }}</p>
                </div>
              </div>
            </a>
            <QBtn
              label="Déconnecter le compte"
              color="red"
              flat
              class="q-mt-md"
              @click="disconnectInstagram"
            />
          </div>

          <div v-else>
            <p>❌ Aucun compte Instagram lié</p>
            <a :href="instagramAuthUrl" class="instagram-button">
              <img src="/assets/images/instagram.svg" alt="Instagram" class="instagram-icon" />
              Lier un compte Instagram
            </a>
          </div>

          <div v-if="instagramError" class="text-negative q-mt-sm">
            {{ instagramError }}
          </div>
        </div>
      </div>
    </div>

    <!-- INFOS PROFIL -->
    <div class="card profile-card">
      <div class="card-header">
        <h3>Informations sur le profil</h3>
      </div>
      <div class="card-body">
        <div class="input-group">
          <label for="username">Nom d'utilisateur</label>
          <QInput v-model="profile.username" id="username" label="Nom d'utilisateur" outlined :rules="[val => !!val || 'Le nom d\'utilisateur est requis', val => val.length >= 4 || 'Le nom d\'utilisateur doit contenir au moins 4 caractères', val => val.length <= 50 || 'Le nom d\'utilisateur doit contenir au maximum 50 caractères' ]"/>
        </div>
        <div class="save-button">
          <QBtn label="Modifier" color="primary" @click="saveProfile" />
        </div>
      </div>
    </div>

    <!-- MOT DE PASSE -->
    <div class="card password-card">
      <div class="card-header">
        <h3>Modifier le mot de passe</h3>
      </div>
      <div class="card-body">
        <div class="input-group">
          <label for="current-password">Mot de passe actuel</label>
          <QInput v-model="currentPassword" id="current-password" type="password" label="Mot de passe actuel" outlined ref="currentPasswordRef"/>
        </div>
        <div class="input-group">
          <label for="new-password">Nouveau mot de passe</label>
          <QInput v-model="newPassword" id="new-password" type="password" label="Nouveau mot de passe" outlined :rules="[val => !!val || 'Le mot de passe est requis', val => val.length >= 6 || 'Le mot de passe doit contenir au moins 6 caractères', val => val.length <= 255 || 'Le mot de passe doit contenir au maximum 255 caractères' ]" ref="newPasswordRef" />
        </div>
        <div class="input-group">
          <label for="confirm-password">Confirmer le nouveau mot de passe</label>
          <QInput v-model="confirmPassword" id="confirm-password" type="password" label="Confirmer le nouveau mot de passe" outlined :rules="[passwordMatchRule]" ref="confirmPasswordRef" />
        </div>
        <div class="save-button">
          <QBtn label="Modifier" color="primary" @click="savePassword" />
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
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #e1306c;
  color: white;
  text-decoration: none;
  padding: 10px 15px;
  border-radius: 8px;
  font-weight: bold;
  white-space: nowrap;
  transition: background-color 0.3s ease;
}

.instagram-button:hover {
  background-color: #cc295f;
}

.instagram-icon {
  width: 24px;
  height: 24px;
}

.ig-connected-link {
  text-decoration: none;
  display: block;
  width: fit-content;
}

.ig-connected-box:hover {
  transform: scale(1.02);
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.ig-connected-box {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fff;
  padding: 10px 15px;
  border-radius: 10px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.08);
  width: fit-content;
  cursor: pointer;
  transition: box-shadow 0.2s ease;
}

.ig-connected-icon {
  width: 40px;
  height: 40px;
}

.ig-connected-text {
  font-weight: bold;
  font-size: 1rem;
  margin: 0;
  color: #2e2e2e;
}

.ig-connected-user {
  margin: 0;
  color: #999;
  font-size: 0.9rem;
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

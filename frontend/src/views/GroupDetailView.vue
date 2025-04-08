<script setup>
import { ref, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { QBtn, QDialog, QCard, QCardSection, QCardActions, QInput } from 'quasar'
import router from '@/router'
import { useAuth, useErrorMessage } from '@/components/store'

const route = useRoute()
const group = ref(null)
const workers = ref([])
const isModalOpen = ref(false)
const newUserName = ref('')
const { user } = useAuth()
const owner = ref(null)
const title = ref(null)
const { errorMessage } = useErrorMessage()

const isOwner = (value) => {
  return user.value.id === value?.owner?.id
}

const fetchGroup = async () => {
  try {
    const response = await axios.get(`/groups/${route.params.id}/`)
    group.value = response.data
    workers.value = response.data.workers
    owner.value = response.data.owner
    title.value = group.value.name
  } catch (error) {
    errorMessage.value = 'Erreur lors de la récupération du groupe : ' + error.response?.data.error || error
    router.push('/')
  }
}

const removeWorker = async (userId) => {
  try {
    await axios.put(`/groups/${route.params.id}/remove_user/`, { user_id: userId })
    workers.value = workers.value.filter(user => user.id !== userId)
  } catch (error) {
    errorMessage.value = 'Erreur lors de la suppression du membre : ' + error.response?.data.error || error
  }
}

const addWorker = async () => {
  if (!newUserName.value.trim()) return

  try {
    const response = await axios.put(`/groups/${route.params.id}/add_user/`, { username: newUserName.value })
    workers.value.push(response.data.user)
    newUserName.value = ''
    isModalOpen.value = false
  } catch (error) {
    errorMessage.value = 'Erreur lors de l\'ajout du membre : ' + error.response?.data.error || error
    isModalOpen.value = false
  }
}

onBeforeMount(() => {
  fetchGroup()
})
</script>

<template>
  <main>
    <div class="title">
      <h1>{{title}}</h1>
    </div>
    <div class="group-detail">
      <div class="left-panel-wrapper">
        <div class="left-panel">
          <!-- Section Administrateur -->
          <h5 class="section-title">Administrateur</h5>
          <div v-if="owner" class="owner-item">
            {{ owner.username }}
          </div>

          <!-- Section Community Managers -->
          <h5 class="section-title">Community Managers</h5>
          <div class="workers-list">
            <div v-for="worker in workers" :key="worker.id" class="worker-item">
              <span>{{ worker.username }}</span>
              <QBtn v-if="isOwner(group)" flat dense round color="red" icon="delete" @click="removeWorker(worker.id)" />
            </div>
          </div>
        </div>
        <QBtn v-if="isOwner(group)" rounded label="Ajouter un membre" color="primary" class="add-btn" @click="isModalOpen = true" />
      </div>

      <div class="right-panel"></div>

      <QDialog v-model="isModalOpen">
        <QCard>
          <QCardSection>
          <h5>Ajouter un membre</h5>
        </QCardSection>
        <QCardSection>
          <QInput v-model="newUserName" label="Nom du membre" outlined rounded />
        </QCardSection>
        <QCardActions align="center">
          <QBtn label="Ajouter" rounded color="primary" @click="addWorker" class="modal-btn" />
        </QCardActions>
      </QCard>
      </QDialog>
    </div>
  </main>
</template>

<style scoped lang="scss">
.title {
  text-align: center;
}
.modal-btn {
  width: 90%;
}

.group-detail {
  display: flex;
  height: 70vh;
}

.left-panel-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 25%;
  margin: 15px;
}

.left-panel {
  width: 100%;
  height: 100%;
  background: $secondary;
  display: flex;
  flex-direction: column;
  align-items: space-between;
  overflow-y: scroll;
  border: 1px solid $dark;
  border-radius: 10px;
  padding: 10px;
}

.left-panel::-webkit-scrollbar {
  width: 6px;
}

.left-panel::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 3px;
}

.left-panel::-webkit-scrollbar-track {
  background: transparent;
}

.right-panel {
  width: 75%;
  padding: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  margin: 10px 0;
  text-align: left;
  width: 100%;
  border-bottom: 1px solid $dark;
  padding-bottom: 5px;
}

.workers-list {
  width: 100%;
  margin-bottom: 20px;
  height: 100%;
}

.worker-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.add-btn {
  width: 100%;
  text-align: center;
  margin-top: 20px;
}
</style>

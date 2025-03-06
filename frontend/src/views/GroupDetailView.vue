<script setup>
import { ref, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { QBtn, QDialog, QCard, QCardSection, QCardActions, QInput } from 'quasar'
import router from '@/router'
import { useAuth } from '@/components/useAuth'

const route = useRoute()
const group = ref(null)
const workers = ref([])
const isModalOpen = ref(false)
const newUserName = ref('')
const { user } = useAuth()

const isOwner = (value) => {
  return user.value.id === value?.owner?.id
}

const fetchGroup = async () => {
  try {
    const response = await axios.get(`/groups/${route.params.id}/`)
    group.value = response.data
    workers.value = response.data.workers
  } catch (error) {
    console.error('Erreur lors de la récupération du groupe :', error.response?.data || error)
    router.push('/')
  }
}

const removeWorker = async (userId) => {
  try {
    await axios.put(`/groups/${route.params.id}/remove_user/`, { user_id: userId })
    workers.value = workers.value.filter(user => user.id !== userId)
  } catch (error) {
    console.error('Erreur lors de la suppression du membre :', error.response?.data || error)
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
    console.error('Erreur lors de l\'ajout du membre :', error.response?.data || error)
  }
}

onBeforeMount(() => {
  fetchGroup()
})
</script>

<template>
  <main class="group-detail">
    <div class="left-panel-wrapper">
      <div class="left-panel">
        <div class="workers-list">
          <div v-for="worker in workers" :key="worker.id" class="worker-item">
            <span>{{ worker.username }}</span>
            <QBtn v-if="isOwner(group)" flat dense round color="red" icon="delete" @click="removeWorker(worker.id)" />
          </div>
        </div>
      </div>
      <QBtn v-if="isOwner(group)" rounded label="Ajouter un membre" color="primary" class="add-btn" @click="isModalOpen = true" />
    </div>

    <div class="right-panel">
    </div>

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
  </main>
</template>

<style scoped lang="scss">
.modal-btn {
  width: 90%;
}

.group-detail {
  display: flex;
  height: 100vh;
}

.left-panel-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 25%;
  margin: 15px;
  margin-top: 70px;
  margin-bottom: 70px;
}

.left-panel {
  width: 100%;
  height: 100%;
  background: $secondary;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: scroll;
  border: 2px solid black;
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

.workers-list {
  width: 100%;
  margin-bottom: 20px;
  height: 100%;
}

.worker-item {
  display: flex;
  justify-content: space-between;
  padding: 5px 10px;
  border-radius: 5px;
  margin-bottom: 5px;
}

.add-btn {
  width: 100%;
  text-align: center;
  margin-top: 20px;
}
</style>

<script setup>
import { ref, onBeforeMount, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { QBtn, QDialog, QCard, QCardSection, QCardActions, QInput, QIcon } from 'quasar'
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
const posts = ref([])

const sectionStates = ref({
  unvalidated: false,
  validated: false,
  expired: false,
  published: false
})

const statusLabels = {
  unvalidated: 'En attente de validation',
  validated: 'Validé',
  expired: 'Expiré',
  published: 'Publié'
}

const toggleSection = (key) => {
  sectionStates.value[key] = !sectionStates.value[key]
}

const filteredPosts = computed(() => {
  const grouped = {
    unvalidated: [],
    validated: [],
    expired: [],
    published: []
  }

  for (const post of posts.value) {
    if (grouped[post.status]) {
      grouped[post.status].push(post)
    }
  }

  for (const key in grouped) {
    grouped[key].sort((a, b) => -(new Date(b.date_publication) - new Date(a.date_publication)))
  }

  return grouped
})

const formatDate = (isoString) => {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleString('fr-FR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

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
    posts.value = response.data.posts
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

const createPost = async () => {
  router.push("/create-post/" + group.value.id)
}

const editPost = async (postId) => {
  router.push("/update-post/" + postId)
}

const displayPost = async (postId) => {
  router.push("/display-post/" + postId)
}

const deletePost = async (postId) => {
  try {
    await axios.delete(`/posts/${postId}/`)
    posts.value = posts.value.filter(post => post.id !== postId)
  } catch (error) {
    errorMessage.value = 'Erreur lors de la suppression du post : ' + error.response?.data.error || error
  }
}

onBeforeMount(() => {
  fetchGroup()
})
</script>

<template>
  <main>
    <div class="title">
      <h1>{{ title }}</h1>
    </div>

    <div class="group-detail">
      <div class="left-panel-wrapper">
        <div class="left-panel">
          <h5 class="section-title">Administrateur</h5>
          <div v-if="owner" class="owner-item">{{ owner.username }}</div>

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

      <div class="right-panel">
        <div class="header">
          <QBtn rounded label="New post" color="primary" class="create-post-btn" @click="createPost" />
        </div>

        <div class="posts-list">
          <div
            v-for="(label, key) in statusLabels"
            :key="key"
            class="post-section"
          >
            <div class="section-header" @click="toggleSection(key)">
              <QIcon :name="sectionStates[key] ? 'expand_more' : 'chevron_right'" class="arrow" />
              {{ label }} ({{ filteredPosts[key].length }})
            </div>

            <div v-if="sectionStates[key]">
              <div
                v-for="post in filteredPosts[key]"
                :key="post.id"
                class="post-item"
                @click="displayPost(post.id)"
              >
                <div class="post-content">
                  <h5>{{ post.name }}</h5>
                  <p>Planifié pour {{ formatDate(post.date_publication) }}</p>
                </div>
                <div class="post-actions">
                  <QBtn flat dense round icon="edit" @click.stop="editPost(post.id)" />
                  <QBtn flat dense round color="red" icon="delete" @click.stop="deletePost(post.id)" />
                </div>
              </div>
            </div>
          </div>
        </div>
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
    </div>
  </main>
</template>

<style scoped lang="scss">
.title {
  text-align: center;
}

.title h1 {
  font-size: 3rem;
}

.modal-btn {
  width: 90%;
}

.group-detail {
  display: flex;
  height: 65vh;
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
  display: flex;
  flex-direction: column;
  height: 100%;
}

.header {
  position: sticky;
  top: 0;
  background: $white; // Remplace par #fff si nécessaire
  z-index: 2;
  padding-bottom: 10px;
  text-align: right;
  margin-right: 5px;
}

.posts-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 5px;
  display: flex;
  flex-direction: column;
  gap: 10px;
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

.section-header {
  font-size: 1rem;
  font-weight: bold;
  padding: 10px;
  cursor: pointer;
  background: $secondary;
  border-radius: 8px;
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.arrow {
  font-size: 20px;
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

.create-post-btn {
  align-self: flex-start;
  margin-left: auto;
}

.post-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: $secondary;
  border-radius: 10px;
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  gap: 10px;
  margin: 10px;
}

.post-item:hover {
  transform: scale(1.02);
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.post-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;
  flex: 1;
  padding: 5px;
}

.post-content h5,
.post-content p {
  margin: 0;
  text-align: left;
}

.post-actions {
  display: flex;
  gap: 5px;
}
</style>

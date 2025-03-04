<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { QBtn, QDialog, QCard, QCardSection, QCardActions, QInput, QIcon } from 'quasar';

const isModalOpen = ref(false);
const groupName = ref('');
const groups = ref([]);
const router = useRouter();

const openModal = () => {
  isModalOpen.value = true;
};

const createGroup = async () => {
  if (groupName.value.trim() === '') {
    console.log("Le nom du groupe est requis !");
    return;
  }

  try {
    const response = await axios.post('/groups/', { name: groupName.value });
    console.log('Groupe créé avec succès', response.data);
    isModalOpen.value = false;
    groupName.value = '';
    fetchGroups();
  } catch (error) {
    console.error('Erreur lors de la création du groupe :', error.response?.data || error);
  }
};

const deleteGroup = async (groupId) => {
  try {
    await axios.delete(`/groups/${groupId}/`);
    console.log('Groupe supprimé avec succès');
    fetchGroups();
  } catch (error) {
    console.error('Erreur lors de la suppression du groupe :', error.response?.data || error);
  }
};

const fetchGroups = async () => {
  try {
    const response = await axios.get('/groups/');
    groups.value = response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des groupes :', error.response?.data || error);
  }
};

onMounted(() => {
  fetchGroups();
});
</script>

<template>
  <main>
    <div class="blue-container main">
      <div class="container-header">
        <h4>VOS ÉQUIPES</h4>
        <QBtn rounded label="Créer équipe" color="primary" class="login-btn" @click="openModal" />
      </div>

      <div v-if="groups.length > 0">
        <ul>
          <li v-for="group in groups" :key="group.id" class="group-item">
            <strong>{{ group.name }}</strong>
            <QBtn
              flat
              dense
              round
              color="primary"
              icon="delete"
              @click="deleteGroup(group.id)"
            />
          </li>
        </ul>
      </div>
    </div>

    <QDialog v-model="isModalOpen">
      <QCard class="modal-card">
        <QCardSection>
          <h5>Créer une équipe</h5>
        </QCardSection>
        <QCardSection>
          <QInput v-model="groupName" label="Nom de l'équipe" filled :rules="[val => !!val || 'Le nom est requis']" />
        </QCardSection>
        <QCardActions align="right">
          <QBtn label="Créer" color="primary" @click="createGroup" :disabled="!groupName.trim()" />
        </QCardActions>
      </QCard>
    </QDialog>
  </main>
</template>

<style scoped lang="scss">
.blue-container {
  background-color: $secondary;
  border-radius: 8px;
  padding: 20px;
}

.container-header {
  display: flex;
  justify-content: space-between;
}

.main {
  margin-top: 20px;
  height: 80vh;
}

.modal-card {
  width: 400px;
  padding: 20px;
}

.group-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
}
</style>

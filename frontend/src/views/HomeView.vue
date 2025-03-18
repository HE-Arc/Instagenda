<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { QBtn, QDialog, QCard, QCardSection, QCardActions, QInput } from 'quasar';
import { useAuth, useErrorMessage } from '@/components/store'

const isModalOpen = ref(false);
const groupName = ref('');
const groups = ref([]);
const router = useRouter();
const slideIndex = ref(0);
const itemsPerSlide = 3;
const { user } = useAuth();
const { errorMessage } = useErrorMessage()

const openModal = () => {
  isModalOpen.value = true;
};

const createGroup = async () => {
  if (groupName.value.trim() === '') {
    errorMessage.value = "Le nom du groupe est requis !";
    return;
  }

  try {
    await axios.post('/groups/', { name: groupName.value });
    isModalOpen.value = false;
    groupName.value = '';
    fetchGroups();
  } catch (error) {
    errorMessage.value = 'Erreur lors de la création du groupe : ' + error.response?.data.error || error;
  }
};

const deleteGroup = async (groupId) => {
  try {
    await axios.delete(`/groups/${groupId}/`);
    fetchGroups();
  } catch (error) {
    errorMessage.value = 'Erreur lors de la suppression du groupe : ' + error.response?.data.error || error;
  }
};

const fetchGroups = async () => {
  try {
    const response = await axios.get('/groups/');
    groups.value = response.data;
  } catch (error) {
    errorMessage.value = 'Erreur lors de la récupération des groupes : ' + error.response?.data.error || error;
  }
};

onMounted(() => {
  fetchGroups();
});

const visibleGroups = computed(() => {
  if (groups.value.length === 0) return [];

  const total = groups.value.length;

  if (total <= itemsPerSlide) {
    return groups.value;
  }

  const result = [];
  for (let i = 0; i < itemsPerSlide; i++) {
    result.push(groups.value[(slideIndex.value + i) % total]);
  }

  return result;
});

const nextSlide = () => {
  if (groups.value.length > itemsPerSlide) {
    slideIndex.value = (slideIndex.value + 1) % groups.value.length;
  }
};

const prevSlide = () => {
  if (groups.value.length > itemsPerSlide) {
    slideIndex.value = (slideIndex.value - 1 + groups.value.length) % groups.value.length;
  }
};

const isOwner = (group) => {
  return group.owner.id === user.value.id;
};

</script>

<template>
  <main>
    <div class="main-container main">
      <div class="container-header">
        <h4>VOS ÉQUIPES</h4>
        <QBtn rounded label="Créer équipe" color="primary" class="login-btn" @click="openModal" />
      </div>

      <div v-if="groups.length > 0" class="carousel-container">
        <QBtn flat dense round icon="chevron_left" color="primary" class="carousel-btn left" @click="prevSlide" />

        <div class="card-container">
          <QCard v-for="group in visibleGroups" :key="group.id" @click="router.push(`/groups/${group.id}`)" class="team-card">
            <div class="card-header">
              <h5 class="team-name">{{ group.name }}</h5>
              <QBtn v-if="isOwner(group)" flat dense round color="primary" icon="delete"
              class="delete-btn" @click.stop="deleteGroup(group.id)"/>
            </div>

            <div class="role-label">
              {{ isOwner(group) ? 'Administrateur' : 'Community manager' }}
            </div>
          </QCard>
        </div>

        <QBtn flat dense round icon="chevron_right" color="primary" class="carousel-btn right" @click="nextSlide" />
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
.main-container {
  background-color: $secondary;
  border-radius: 8px;
  padding: 20px;
  border : solid 1px;
  border-color : $dark;
}

.container-header {
  display: flex;
  justify-content: space-between;
}

.main {
  margin-top: 20px;
  height: 80vh;
}

.card-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
  gap: 20px;
  height: 100%;
}

.carousel-container {
  width: 90%;
  height: 75%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 50px auto;
}

.team-card {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 15px;
  border-radius: 12px;
  text-align: center;
  background-color: $white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;

  display: flex;
  flex-direction: column;
  justify-content: flex-start;

  &:hover {
    transform: scale(1.03);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.role-label {
  margin-top: auto; /* Pousse ce texte en bas */
  font-size: 14px;
  font-weight: bold;
  color: $dark;
  text-align: center;
}

.team-name {
  flex-grow: 1;
  text-align: center;
  font-size: 16px;
  font-weight: bold;
  color: $dark;
  margin: 0 auto;
}

.delete-btn {
  position: absolute;
  top: 10px;
  right: 10px;
}

.carousel-btn {
  background: none;
  border: none;
  cursor: pointer;
}

.left {
  margin-right: 10px;
}

.right {
  margin-left: 10px;
}

.modal-card {
  width: 400px;
  padding: 20px;
}
</style>

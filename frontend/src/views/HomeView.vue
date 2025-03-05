<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { QBtn, QDialog, QCard, QCardSection, QCardActions, QInput } from 'quasar';

const isModalOpen = ref(false);
const groupName = ref('');
const groups = ref([]);
const router = useRouter();
const slideIndex = ref(0);
const itemsPerSlide = 3;

const openModal = () => {
  isModalOpen.value = true;
};

const createGroup = async () => {
  if (groupName.value.trim() === '') {
    console.log("Le nom du groupe est requis !");
    return;
  }

  try {
    await axios.post('/groups/', { name: groupName.value });
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

// Gère le carrousel infini avec un décalage d'un élément à la fois
const visibleGroups = computed(() => {
  if (groups.value.length === 0) return [];

  const total = groups.value.length;

  // Si on a moins de 3 groupes, on affiche uniquement ceux disponibles sans répétition
  if (total <= itemsPerSlide) {
    return groups.value;
  }

  // Sinon, on applique l'effet de boucle infinie
  const result = [];
  for (let i = 0; i < itemsPerSlide; i++) {
    result.push(groups.value[(slideIndex.value + i) % total]);
  }

  return result;
});

// Défilement infini uniquement si on a plus de 3 groupes
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
</script>

<template>
  <main>
    <div class="blue-container main">
      <div class="container-header">
        <h4>VOS ÉQUIPES</h4>
        <QBtn rounded label="Créer équipe" color="primary" class="login-btn" @click="openModal" />
      </div>

      <!-- Carrousel des équipes -->
      <div v-if="groups.length > 0" class="carousel-container">
        <QBtn flat dense round icon="chevron_left" class="carousel-btn left" @click="prevSlide" />

        <div class="card-container">
          <QCard v-for="group in visibleGroups" :key="group.id" class="team-card">
            <QCardSection>
              <h5 class="team-name">{{ group.name }}</h5>
            </QCardSection>
            <QCardActions align="right">
              <QBtn flat dense round color="negative" icon="delete" @click="deleteGroup(group.id)" />
            </QCardActions>
          </QCard>
        </div>

        <QBtn flat dense round icon="chevron_right" class="carousel-btn right" @click="nextSlide" />
      </div>

      <div v-else>
        <p>Aucun groupe trouvé.</p>
      </div>
    </div>

    <!-- Modale pour la création d'un groupe -->
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

.carousel-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 75%;
  margin: 20px auto;
}

.card-container {
  display: flex;
  justify-content: center;
  gap: 40px;
  max-width: 600px;
}

.team-card {
  width: 200px;
  padding: 15px;
  border-radius: 12px;
  text-align: center;
  background-color: #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.team-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
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

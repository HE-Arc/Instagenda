<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { QBtn, QDialog, QCard, QCardSection, QCardActions, QInput } from 'quasar';

const isModalOpen = ref(false);
const groupName = ref('');
const router = useRouter();

const openModal = () => {
  isModalOpen.value = true;
};

const createGroup = async () => {
  // Assurez-vous que le champ 'groupName' est non vide avant de soumettre
  if (groupName.value.trim() === '') {
    // Afficher un message ou ne rien faire si le champ est vide
    console.log("Le nom du groupe est requis !");
    return;
  }

  // Effectuer l'appel à l'API pour créer le groupe
  try {
    const response = await axios.post('/groups/', { name: groupName.value });
    console.log('Groupe créé avec succès', response.data);
    isModalOpen.value = false;
    router.push('/'); // Redirection après création
  } catch (error) {
    console.error('Erreur lors de la création du groupe :', error.response?.data || error);
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
    </div>

    <QDialog v-model="isModalOpen">
      <QCard class="modal-card">
        <QCardSection>
          <h5>Créer une équipe</h5>
        </QCardSection>
        <QCardSection>
          <!-- Le champ 'groupName' est maintenant requis -->
          <QInput v-model="groupName" label="Nom de l'équipe" filled :rules="[val => !!val || 'Le nom est requis']" />
        </QCardSection>
        <QCardActions align="right">
          <!-- Désactiver le bouton si le champ est vide -->
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
</style>

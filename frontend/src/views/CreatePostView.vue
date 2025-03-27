<script setup>
import { QBtn, QInput, QDate, QTime } from 'quasar';
import { ref } from 'vue';
import { useErrorMessage } from '@/components/store'
import { useRoute } from 'vue-router';
import axios from 'axios';

const postName = ref('');
const postContent = ref('');
const postImage = ref('');
const postDate = ref('');
const postTime = ref('');
const { errorMessage } = useErrorMessage();
const route = useRoute();

const postPost = async () => {
  if (!postName.value.trim() || !postContent.value.trim() || !postImage.value.trim() || !postDate.value || !postTime.value) {
    return;
  }

  const formattedDateTime = `${postDate.value} ${postTime.value}`;
  const date = new Date(formattedDateTime);
  const formattedDate = date.toISOString().slice(0, 19).replace('T', ' ').replace(/:\d{2}$/, '');

  console.log(formattedDate);

  const now = new Date();
  if (date < now) {
    errorMessage.value = 'La date doit être dans le futur !';
    return;
  }

  try {
    let response = await axios.post('/posts/', {
      name: postName.value,
      caption: postContent.value,
      image_url: postImage.value,
      date_publication: formattedDate,
      group_id: route.params.id,
    });
    console.log(response.data)
    postName.value = '';
    postContent.value = '';
    postImage.value = '';
    postDate.value = '';
    postTime.value = '';
  } catch (error) {
    errorMessage.value = 'Erreur lors de la création du post : ' + error.response?.data.error || error;
  }
};
</script>
<template>
  <main class="edit-post-container">
    <h5>Création de post</h5>
    <QInput v-model="postName" label="Nom du post" filled :rules="[val => !!val || 'Le nom est requis']" class="q-mb-md" />
    <QInput v-model="postContent" label="Contenu du post" filled :rules="[val => !!val || 'Le contenu est requis']" type="textarea" class="q-mb-md" />
    <QInput v-model="postImage" label="Image du post" filled :rules="[val => !!val || 'L\'image est requise']" class="q-mb-md" type="url"/>
    <div class="date-time-container">
      <QDate v-model="postDate" filled :rules="[val => !!val || 'La date est requise']" class="date-picker full-width" />
      <QTime v-model="postTime" filled :rules="[val => !!val || 'L\'heure est requise']" class="time-picker full-width" />
    </div>
    <QBtn label="Créer" color="primary" @click="postPost" :disabled="!postName.trim() || !postContent.trim() || !postImage.trim() || !postDate || !postTime" class="submit-btn q-mt-md" />
  </main>
</template>

<style scoped>
.edit-post-container {
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
  margin-top: 20px;
  margin-bottom: 20px;
}

.date-time-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
.block {
  display: block;
}

.full-width {
  width: 100%;
}

.submit-btn {
  width: 100%;
  margin-top: 1.5rem;
}

@media (min-width: 768px) {
  .date-time-container {
    flex-direction: row;
    gap: 1rem;
  }

  .input-wrapper {
    width: 50%;
  }
}
</style>

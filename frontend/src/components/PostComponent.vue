<script setup>
import { QBtn, QInput, QDate, QTime, QUploader } from 'quasar';
import { ref } from 'vue';
import { useErrorMessage } from '@/components/store'
import { useRoute, useRouter } from 'vue-router';
import draggable from 'vuedraggable';
import axios from 'axios';

const props = defineProps({
  title: {
    type: String,
    default: 'Créer un post',
  },
  update: {
    type: Boolean,
    default: false,
  },
  postid: {
    type: Number,
    default: null,
  }
});

const postName = ref('');
const postContent = ref('');
const postImage = ref('');
const postDate = ref('');
const postTime = ref('');
const files = ref([]);
const { errorMessage } = useErrorMessage();
const route = useRoute();
const router = useRouter();

if (props.update) {
  const fetchPost = async () => {
    try {
      const response = await axios.get(`/posts/${props.postid}/`);
      postName.value = response.data.name;
      postContent.value = response.data.caption;
      postImage.value = response.data.image_url;
      console.log(response.data.date_publication);
      const [datePart, timePart] = response.data.date_publication.split('T');
      postDate.value = datePart.replace(/-/g, '/');
      postTime.value = timePart.slice(0, 5);
    } catch (error) {
      errorMessage.value = 'Erreur lors de la récupération du post : ' + error.response?.data.error || error;
    }
  };
  fetchPost();
}

const handleAction = async () => {
  if (!props.update) {
    if (!postName.value.trim() || !postContent.value.trim() || !postImage.value.trim() || !postDate.value || !postTime.value) {
      return;
    }

    const formattedDateTime = `${postDate.value} ${postTime.value}`;
    const date = new Date(formattedDateTime);
    const formattedDate = date.toISOString().slice(0, 19).replace('T', ' ').replace(/:\d{2}$/, '');

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
  } else {
    console.log('Update post');
  }
  router.push('/group/');
};

const onFilesAdded = (newFiles) => {
  files.value = files.value.concat(Array.from(newFiles));
};

const onFilesRemoved = (removedFiles) => {
  files.value = files.value.filter(file => !removedFiles.includes(file));
};

const getObjectUrl = (file) => {
  return URL.createObjectURL(file);
};
</script>
<template>
  <main class="edit-post-container">
    <h5>{{props.title}}</h5>
    <QInput v-model="postName" label="Nom du post" filled :rules="[val => !!val || 'Le nom est requis']" class="q-mb-md" />
    <QInput v-model="postContent" label="Contenu du post" filled :rules="[val => !!val || 'Le contenu est requis']" type="textarea" class="q-mb-md" />
    <q-uploader
      label="Photos du post"
      @added="onFilesAdded"
      @removed="onFilesRemoved"
      :auto-upload="false"
      multiple
      no-thumbnails
      hide-upload-btn
      style="height: 150px; overflow-y: auto; width: 100%; margin-bottom: 20px;"
    />
    <h6>Photos ajoutées</h6>
    <p v-if="files.length === 0">Aucune photo ajoutée</p>
    <p v-else>Faites glisser pour réorganiser</p>
    <QInput v-model="postImage" label="Image du post" filled :rules="[val => !!val || 'L\'image est requise']" class="q-mb-md" type="url"/>
    <draggable v-model="files" class="q-mt-md" :itemKey="(item) => item.name">
      <template #item="{ element }">
        <div class="q-pa-sm q-mb-sm image-container">
          <img :src="getObjectUrl(element)" alt="Aperçu" class="draggable-image" />
          <p>{{ element.name }}</p>
        </div>
      </template>
    </draggable>
    <div class="date-time-container">
      <QDate v-model="postDate" filled :rules="[val => !!val || 'La date est requise']" class="date-picker full-width" />
      <QTime v-model="postTime" filled :rules="[val => !!val || 'L\'heure est requise']" class="time-picker full-width" />
    </div>
    <QBtn :label="props.update ? 'Mettre à jour' : 'Créer'" color="primary" @click="handleAction" :disabled="!postName.trim() || !postContent.trim() || !files.length || !postDate || !postTime" class="submit-btn q-mt-md" />
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

.image-container {
  text-align: center;
}

.draggable-image {
  max-width: 200px;
  max-height: 200px;
  display: block;
  margin: 0 auto;
}
</style>

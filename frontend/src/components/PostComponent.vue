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
const groupId = ref(null);
const files = ref([]);
const existingImages = ref([]);
const uploaderRef = ref(null);
const { errorMessage } = useErrorMessage();
const route = useRoute();
const router = useRouter();

// Function to convert URL to File object
const urlToFile = async (url, filename) => {
  try {
    const apiBaseUrl = import.meta.env.VITE_API_URL;
    const fullUrl = `${apiBaseUrl}${url}`;

    const response = await fetch(fullUrl);
    const blob = await response.blob();
    return new File([blob], filename, { type: blob.type });
  } catch (error) {
    console.error("Erreur lors de la conversion de l'URL en fichier:", error);
    return null;
  }
};

if (props.update) {
  const fetchPost = async () => {
    try {
      const response = await axios.get(`/posts/${props.postid}/`);
      postName.value = response.data.name;
      postContent.value = response.data.caption;

      groupId.value = response.data.group_owner;

      const utcDate = new Date(response.data.date_publication);
      const year = utcDate.getFullYear();
      const month = String(utcDate.getMonth() + 1).padStart(2, '0');
      const day = String(utcDate.getDate()).padStart(2, '0');

      postDate.value = `${year}/${month}/${day}`;
      postTime.value = utcDate.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit', hour12: false });

      // Get existing images
      if (response.data.images && response.data.images.length > 0) {
        existingImages.value = response.data.images;

        // Convert URLs to File objects for the uploader
        const imageFiles = await Promise.all(
          response.data.images.map(async (img) => {
            const filename = img.image_url.split('/').pop();
            const file = await urlToFile(img.image_url, filename);
            if (file) {
              file.id = img.id;
              file.order = img.order;
              return file;
            }
            return null;
          })
        );

        // add files to the uploader
        setTimeout(() => {
          if (uploaderRef.value) {
            uploaderRef.value.addFiles(imageFiles.filter(f => f !== null).sort((a, b) => a.order - b.order));
          }
        }, 500);
      }
    } catch (error) {
      errorMessage.value = 'Erreur lors de la récupération du post : ' + error.response?.data.error || error;
    }
  };
  fetchPost();
}

const handleAction = async () => {
  if (!postName.value.trim() || !postContent.value.trim() || !postDate.value || !postTime.value || files.value.length === 0) {
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
    const formData = new FormData();
    formData.append('name', postName.value);
    formData.append('caption', postContent.value);
    formData.append('date_publication', formattedDate);

    // Add all images in the order of the draggable
    files.value.forEach((file) => {
      formData.append('uploaded_images', file);
    });

    if (!props.update) {
      // Create a new post
      formData.append('group_id', route.params.id);
      await axios.post('/posts/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      // Reset form fields after creation
      postName.value = '';
      postContent.value = '';
      postImage.value = '';
      postDate.value = '';
      postTime.value = '';
      files.value = [];

      router.push('/groups/' + route.params.id);
    } else {
      await axios.put(`/posts/${props.postid}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      router.push('/groups/' + groupId.value);
    }
  } catch (error) {
    const action = props.update ? 'la mise à jour' : 'la création';
    errorMessage.value = `Erreur lors de ${action} du post : ` + (error.response?.data.error || error);
  }
};

const onFilesAdded = (newFiles) => {
  const uniqueNewFiles = Array.from(newFiles).filter(newFile => {
    return !files.value.some(existingFile =>
      existingFile.name === newFile.name &&
      existingFile.size === newFile.size
    );
  });

  if (uniqueNewFiles.length < newFiles.length) {
    errorMessage.value = 'Certaines images seront ignorées car elles sont déjà présentes dans la liste.';
  }

  files.value = files.value.concat(uniqueNewFiles);
};

const onFilesRemoved = (removedFiles) => {
  // Delete the _objectUrl property to avoid memory leaks
  removedFiles.forEach(file => {
    if (file._objectUrl) {
      URL.revokeObjectURL(file._objectUrl);
      delete file._objectUrl;
    }
  });
  files.value = files.value.filter(file => !removedFiles.includes(file));
};

// Save object URLs to avoid multiple creations
const getObjectUrl = (file) => {
  if (!file._objectUrl) {
    file._objectUrl = URL.createObjectURL(file);
  }
  return file._objectUrl;
};
</script>
<template>
  <main class="edit-post-container">
    <QBtn
      flat
      dense
      icon="arrow_back"
      label="Retour"
      @click="router.back()"
      class="back-btn"
      color="primary"
    />
    <h5 class="title">{{props.title}}</h5>
    <QInput v-model="postName" label="Nom du post" filled :rules="[val => !!val || 'Le nom est requis']" class="q-mb-md" />
    <QInput v-model="postContent" label="Contenu du post" filled :rules="[val => !!val || 'Le contenu est requis']" type="textarea" class="q-mb-md" />
    <q-uploader
      ref="uploaderRef"
      label="Photos du post (format recommandé 1:1)"
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

.title {
  margin-bottom: 20px;
}

.back-btn {
  align-self: flex-start;
  margin-bottom: 10px;
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

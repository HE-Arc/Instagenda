<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { QCarousel, QCarouselSlide, QBtn } from 'quasar';

const props = defineProps({
  postid: {
    type: Number,
    required: true
  }
});

const router = useRouter();
const post = ref(null);
const images = ref([]);
const activeSlide = ref(0);

const fetchPost = async () => {
  try {
    const response = await axios.get(`/posts/${props.postid}/`);
    post.value = response.data;

    // Reconstituer les URLs complètes des images
    images.value = (response.data.images || []).map((img) => ({
      id: img.id,
      url: new URL(img.image_url, import.meta.env.VITE_API_URL).href
    }));
  } catch (error) {
    console.error('Erreur lors de la récupération du post :', error);
  }
};

onMounted(() => {
  fetchPost();
});

const formatDate = (isoString) => {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleString('fr-FR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};
</script>

<template>
  <main class="preview-container">
    <QBtn
      flat
      dense
      icon="arrow_back"
      label="Retour"
      @click="router.back()"
      class="back-btn"
      color="primary"
    />

    <div v-if="post" class="card">
      <!-- Images Carousel -->
      <QCarousel
        v-if="images.length"
        :key="images.length"
        v-model="activeSlide"
        animated
        swipeable
        infinite
        control-color="white"
        navigation
        height="400px"
        class="carousel"
      >
        <QCarouselSlide
          v-for="(img, index) in images"
          :key="img.id"
          :name="index"
          :img-src="img.url"
        />
      </QCarousel>

      <!-- Post Details -->
      <div class="post-details">
        <h2>{{ post.name }}</h2>
        <p class="caption">{{ post.caption }}</p>
        <p class="date">Planifié pour : {{ formatDate(post.date_publication) }}</p>
      </div>
    </div>

    <div v-else class="loading">
      Chargement...
    </div>
  </main>
</template>

<style scoped>
.preview-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px 10px;
}

.back-btn {
  margin-bottom: 15px;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.carousel {
  border-bottom: 1px solid #eee;
}

.post-details {
  padding: 20px;
}

.post-details h2 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.caption {
  font-size: 1rem;
  margin-bottom: 15px;
  color: #333;
}

.date {
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
}

.loading {
  text-align: center;
  color: #ccc;
}
</style>

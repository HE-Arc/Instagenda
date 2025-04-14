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
        class="carousel square-carousel"
      >
        <QCarouselSlide
          v-for="(img, index) in images"
          :key="img.id"
          :name="index"
          class="carousel-slide"
        >
          <img :src="img.url" class="carousel-image" />
        </QCarouselSlide>
      </QCarousel>

      <!-- Custom Carousel Controls (dots) -->
      <div class="carousel-controls" v-if="images.length > 1">
        <span
          v-for="(img, index) in images"
          :key="'dot-' + img.id"
          class="dot"
          :class="{ active: activeSlide === index }"
          @click="activeSlide = index"
        ></span>
      </div>

      <!-- Post Details -->
      <div class="post-details">
        <p class="caption">{{ post.caption }}</p>
        <p class="date">Planifié pour : {{ formatDate(post.date_publication) }}</p>
      </div>
    </div>

    <div v-else class="loading">
      <p>Chargement...</p>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { QCarousel, QCarouselSlide, QBtn } from 'quasar';
import { useErrorMessage } from '@/components/store';

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
const { errorMessage } = useErrorMessage();

const fetchPost = async () => {
  try {
    const response = await axios.get(`/posts/${props.postid}/`);
    post.value = response.data;

    images.value = (response.data.images || []).map((img) => ({
      id: img.id,
      url: new URL(img.image_url, import.meta.env.VITE_API_URL).href
    }));
  } catch (error) {
    errorMessage.value = 'Ce post n\'existe pas ou a été supprimé.';
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

<style scoped lang="scss">
.preview-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px 10px;
}

.back-btn {
  margin-bottom: 15px;
}

.card {
  background: $white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.carousel {
  border-bottom: 1px solid $white;
}

.square-carousel {
  aspect-ratio: 1 / 1;
  height: auto !important;
}

.carousel-slide {
  padding: 10px;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Custom Dots */
.carousel-controls {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 20px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: $secondary;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.dot.active {
  background-color: $primary;
}

.post-details {
  padding: 0px 15px 0px 15px;
}

.caption {
  font-size: 1rem;
  margin-bottom: 15px;
  color: $dark;
}

.date {
  font-size: 0.9rem;
  color: $dark;
  font-style: italic;
}

.loading {
  text-align: center;
  color: $dark;
}
</style>

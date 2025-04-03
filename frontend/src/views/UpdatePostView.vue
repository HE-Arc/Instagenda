<script setup>
import PostComponent from '@/components/PostComponent.vue';
import { useRoute } from 'vue-router';

const route = useRoute();
</script>
<template>
  <PostComponent title="Mettre à jour un post" :update="true" :postid="Number(route.params.id)" />
</template>

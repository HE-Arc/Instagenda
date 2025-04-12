<script setup>
import PostComponent from '@/components/PostComponent.vue';
import { useRoute } from 'vue-router';

const route = useRoute();
</script>
<template>
  <PostComponent title="Modifer le post" :update="true" :postid="Number(route.params.id)" />
</template>

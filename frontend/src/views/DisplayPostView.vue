<script setup>
import DisplayPostComponent from '@/components/DisplayPostComponent.vue';
import PostComponent from '@/components/DisplayPostComponent.vue';
import { useRoute } from 'vue-router';

const route = useRoute();
</script>
<template>
  <DisplayPostComponent title="Modifer le post" :postid="Number(route.params.id)" />
</template>

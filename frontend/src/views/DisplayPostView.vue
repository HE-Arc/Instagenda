<script setup>
import DisplayPostComponent from '@/components/DisplayPostComponent.vue';
import { useRoute } from 'vue-router';

const route = useRoute();
</script>
<template>
  <DisplayPostComponent :postid="Number(route.params.id)" />
</template>

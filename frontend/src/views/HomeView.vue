<script setup>
import router from '@/router'
import { QBtn } from 'quasar'
</script>

<template>
  <main>
    <QBtn label="profile" @click="router.push('/user')"/>
  </main>
</template>
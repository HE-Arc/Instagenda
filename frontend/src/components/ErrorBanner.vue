<script setup>
import { computed, watch } from 'vue'
import { QBanner, QBtn } from 'quasar'
import { useErrorMessage } from '@/components/store'

const { errorMessage } = useErrorMessage()

const isVisible = computed(() => errorMessage.value !== '')

const closeBanner = () => {
  errorMessage.value = ""
}

watch(errorMessage, (newValue) => {
  if (newValue) {
    setTimeout(() => {
      closeBanner()
    }, 5000)
  }
})
</script>

<template>
  <QBanner
    v-if="isVisible"
    class="error-banner"
    rounded
    dense
    inline-actions
  >
    {{ errorMessage }}
    <template v-slot:action>
      <QBtn flat label="Fermer" @click="closeBanner" />
    </template>
  </QBanner>
</template>

<style scoped>
.error-banner {
  position: fixed;
  top: 60px;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
  max-width: 600px;
  z-index: 1000;
  background-color: #C10015;
  color: white;
}
</style>

<!-- filename: vue_js_project/src/components/AnnouncementCard.vue -->
<template>
  <div class="border rounded p-4 shadow mb-4 bg-white dark:bg-gray-800 dark:text-white">
    <h2 class="font-bold text-lg">{{ title }}</h2>
    <p class="mt-2">{{ body }}</p>
    <small class="text-gray-500 dark:text-gray-400">
      By: {{ createdBy.first_name }} {{ createdBy.last_name }} • {{ formattedDate }}
    </small>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  body: {
    type: String,
    required: true
  },
  createdBy: {
    type: Object,
    required: true
  },
  createdAt: {
    type: String,
    required: true
  }
})

// Compute formatted date
const formattedDate = computed(() => {
  const date = new Date(props.createdAt)
  return date.toLocaleString()
})
</script>

<style scoped>
/* Add any component-specific styles here */
</style>

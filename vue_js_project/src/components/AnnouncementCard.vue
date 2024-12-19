<!-- filename: vue_js_project/src/components/AnnouncementCard.vue -->
<template>
  <div class="border rounded p-4 shadow mb-4 bg-white dark:bg-gray-800 dark:text-white">
    <h2 class="font-bold text-lg">{{ title }}</h2>
    <p class="mt-2">{{ body }}</p>
    <small class="text-gray-500 dark:text-gray-400">By: {{ createdBy }} • {{ createdAt }}</small>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
defineProps({
  title: String,
  body: String,
  createdBy: String,
  createdAt: String
})
</script>

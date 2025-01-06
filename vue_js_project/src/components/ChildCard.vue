<!-- filename: vue_js_project/src/components/ChildCard.vue -->
<template>
    <div class="border rounded p-4 shadow mb-4 bg-white dark:bg-gray-800 dark:text-white">
      <h2 class="font-bold text-lg">{{ firstName }} {{ lastName }}</h2>
      <p class="mt-2">Class: {{ className }}</p>
      <small class="text-gray-500 dark:text-gray-400">
        Added on: {{ formattedDate }}
      </small>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    firstName: {
      type: String,
      required: true
    },
    lastName: {
      type: String,
      required: true
    },
    className: {
      type: String,
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
    return date.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  })
  </script>
  
  <style scoped>
  /* Add any component-specific styles here */
  </style>
  
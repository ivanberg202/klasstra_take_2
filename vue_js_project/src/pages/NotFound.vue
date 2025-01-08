<!-- filename: src/pages/NotFound.vue -->
<template>
    <DefaultLayout>
      <div class="flex flex-col items-center justify-center min-h-screen">
        <h1 class="text-4xl font-bold mb-4">404 - Page Not Found</h1>
        <p class="mb-4">The page you are looking for does not exist.</p>
        <router-link to="/login" class="text-primary hover:underline">Go to Login</router-link>
      </div>
    </DefaultLayout>
  </template>
  
  <script setup>
  import DefaultLayout from '@/layouts/DefaultLayout.vue';
  </script>
  
  <style scoped>
  /* Add any specific styles here */
  </style>
  
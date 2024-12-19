<!-- filename: vue_js_project/src/App.vue -->
<template>
  <div class="bg-white dark:bg-gray-900 min-h-screen text-gray-900 dark:text-white">
    <Navbar />
    <router-view />
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
</script>

<style scoped>
</style>

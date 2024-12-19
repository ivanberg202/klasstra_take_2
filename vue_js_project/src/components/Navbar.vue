<!-- filename: vue_js_project/src/components/Navbar.vue -->
<template>
  <nav class="p-4 flex justify-between items-center bg-primary dark:bg-gray-800">
    <div class="text-white font-bold">Klasstra</div>
    <div class="flex items-center space-x-4">
      <ThemeToggle />
      <button @click="logout" class="bg-white text-black px-3 py-1 rounded">Logout</button>
    </div>
  </nav>
</template>

<script setup>
import { useStore } from 'vuex'
import ThemeToggle from './ThemeToggle.vue'
const store = useStore()

function logout() {
  store.commit('setAuth', {token:null, role:null})
  location.href = '/login'
}
</script>

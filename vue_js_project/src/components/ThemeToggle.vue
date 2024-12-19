<!-- filename: vue_js_project/src/components/ThemeToggle.vue -->
<template>
  <button @click="toggle" class="px-3 py-1 bg-secondary text-white rounded">
    {{ isDark ? 'Light Mode' : 'Dark Mode' }}
  </button>
</template>

<script setup>
import { useStore } from 'vuex'
const store = useStore()
const isDark = computed(() => store.state.darkMode)
function toggle(){ store.commit('toggleDarkMode') }
</script>

<!-- filename: vue_js_project/src/components/ThemeToggle.vue -->
<template>
  <button
    @click="toggleDarkMode"
    class="px-4 py-2 rounded shadow-md text-white"
    :class="isDark ? 'bg-secondary' : 'bg-primary'"
  >
    {{ isDark ? 'Light Mode' : 'Dark Mode' }}
  </button>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const isDark = computed(() => store.state.darkMode);

// Toggle dark mode and update Vuex + localStorage
const toggleDarkMode = () => {
  store.commit('toggleDarkMode');
};
</script>

<style scoped>
button {
  transition: background-color 0.3s ease, color 0.3s ease;
}
</style>

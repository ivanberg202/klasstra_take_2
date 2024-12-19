<!-- ThemeToggle.vue -->
<template>
  <button @click="toggle" class="px-3 py-1 bg-secondary text-white rounded">
    {{ isDark ? 'Light Mode' : 'Dark Mode' }}
  </button>
</template>

<script setup>
import { computed } from 'vue'; // Import computed
import { useStore } from 'vuex';

const store = useStore();
const isDark = computed(() => store.state.darkMode);

function toggle() {
  store.commit('toggleDarkMode');
}
</script>

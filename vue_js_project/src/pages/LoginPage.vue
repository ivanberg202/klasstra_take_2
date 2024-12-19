<!-- filename: vue_js_project/src/pages/LoginPage.vue -->
<template>
  <DefaultLayout>
    <div class="max-w-md mx-auto bg-white dark:bg-gray-800 p-6 rounded shadow">
      <h1 class="text-xl font-bold mb-4">Login</h1>
      <form @submit.prevent="login">
        <input
          v-model="username"
          placeholder="Username or Email"
          class="w-full mb-2 p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
          autocomplete="username"
        />
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="w-full mb-4 p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
          autocomplete="current-password"
        />
        <button type="submit" class="bg-primary text-white w-full p-2 rounded">
          Login
        </button>
      </form>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import DefaultLayout from '../layouts/DefaultLayout.vue';

const store = useStore();
const username = ref('');
const password = ref('');

async function login() {
  try {
    const res = await axios.post('/auth/login', { username: username.value, password: password.value });
    const tokenData = parseJwt(res.data.access_token);
    store.commit('setAuth', { token: res.data.access_token, role: tokenData.role });
    redirectByRole();
  } catch (err) {
    console.error('Login failed:', err);
  }
}

function parseJwt(token) {
  const base64Url = token.split('.')[1];
  return JSON.parse(decodeURIComponent(atob(base64Url).split('').map(c => {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join('')));
}

function redirectByRole() {
  if (store.state.role === 'teacher') location.href = '/teacher';
  else if (store.state.role === 'parent' || store.state.role === 'class_rep') location.href = '/parent';
  else if (store.state.role === 'admin') location.href = '/admin';
}
</script>

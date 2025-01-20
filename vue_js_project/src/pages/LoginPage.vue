<!-- filename: vue_js_project/src/pages/LoginPage.vue -->
<template>
  <DefaultLayout>
    <div class="max-w-md mx-auto bg-white dark:bg-gray-800 p-6 rounded shadow">
      <h1 class="text-xl font-bold mb-4 text-gray-900 dark:text-gray-100">Login</h1>
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
      <div class="mt-4 text-center">
        <p class="text-gray-600 dark:text-gray-400">
          Don't have an account?
          <a href="/register" class="text-primary hover:underline">Register here</a>
        </p>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref } from 'vue';
import { useStore } from 'vuex';
import axios, { setAuthToken } from '../plugins/axios.js';
import DefaultLayout from '../layouts/DefaultLayout.vue';

const store = useStore();
const username = ref('');
const password = ref('');

/**
 * Convert JWT into decoded JSON data
 */
function parseJwt(token) {
  const base64Url = token.split('.')[1];
  return JSON.parse(decodeURIComponent(
    atob(base64Url)
      .split('')
      .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
      .join('')
  ));
}

/**
 * Redirect based on role
 */
function redirectByRole() {
  if (store.state.role === 'teacher') location.href = '/teacher';
  else if (store.state.role === 'parent' || store.state.role === 'class_rep') location.href = '/parent';
  else if (store.state.role === 'admin') location.href = '/admin';
}

/**
 * Sends form data to match your OAuth2PasswordRequestForm backend
 */
async function login() {
  try {
    // Convert credentials to form-encoded data
    const formData = new URLSearchParams();
    formData.append('username', username.value);
    formData.append('password', password.value);

    // POST with 'application/x-www-form-urlencoded'
    const res = await axios.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    const token = res.data.access_token;
    setAuthToken(token); // Store the token in Axios defaults

    // Decode and store role in Vuex
    const tokenData = parseJwt(token);
    store.commit('setAuth', { token, role: tokenData.role });

    // Redirect to the appropriate dashboard
    redirectByRole();
  } catch (err) {
    console.error('Login failed:', err);
    // You could show a toast or error message here
  }
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>

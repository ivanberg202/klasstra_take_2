<!-- filename: vue_js_project/src/pages/RegisterPage.vue -->
<template>
  <DefaultLayout>
    <div class="max-w-md mx-auto bg-white dark:bg-gray-800 p-6 rounded shadow">
      <h1 class="text-xl font-bold mb-4 text-gray-900 dark:text-gray-100">Register</h1>

      <form @submit.prevent="register">
        <input
          v-model="username"
          placeholder="Username"
          class="w-full mb-2 p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
          required
        />
        <input
          v-model="firstName"
          placeholder="First Name"
          class="w-full mb-2 p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
          required
        />
        <input
          v-model="lastName"
          placeholder="Last Name"
          class="w-full mb-2 p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
          required
        />
        <input
          v-model="email"
          type="email"
          placeholder="Email"
          class="w-full mb-2 p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
          required
        />
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="w-full mb-2 p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
          required
          minlength="8"
          title="Password must be at least 8 characters long and include letters, numbers, and symbols."
        />
        <select
          v-model="role"
          class="w-full mb-4 p-2 border rounded bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600"
          required
        >
          <option disabled value="">Select Role</option>
          <option value="teacher">Teacher</option>
          <option value="parent">Parent</option>
        </select>
        <button
          type="submit"
          class="bg-primary text-white w-full p-2 rounded"
          :disabled="isSubmitting"
        >
          {{ isSubmitting ? 'Registering...' : 'Register' }}
        </button>
      </form>

      <div v-if="successMessage" class="mt-4 text-green-500">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="mt-4 text-red-500">
        {{ errorMessage }}
      </div>

      <div class="mt-4 text-center">
        <p class="text-gray-600 dark:text-gray-400">
          Already have an account?
          <a href="/login" class="text-primary hover:underline">Login here</a>
        </p>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref } from 'vue' // Import ref from Vue
import axios from 'axios'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import { useStore } from 'vuex'
import { setAuthToken } from '../plugins/axios.js' // Ensure this function is exported

const store = useStore()

// Reactive state variables
const username = ref('')
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const role = ref('')
const isSubmitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

// Registration function
async function register() {
  // Reset messages
  successMessage.value = ''
  errorMessage.value = ''

  // Frontend Validation
  if (
    !username.value ||
    !firstName.value ||
    !lastName.value ||
    !email.value ||
    !password.value ||
    !role.value
  ) {
    errorMessage.value = 'All fields are required.'
    return
  }

  isSubmitting.value = true

  try {
    // Make the registration request
    await axios.post('/users', {
      username: username.value,
      first_name: firstName.value,
      last_name: lastName.value,
      email: email.value,
      password: password.value,
      role: role.value
    })

    // After successful registration, perform auto-login
    const loginResponse = await axios.post('/auth/login', {
      username: username.value, // Assuming username is used for login
      password: password.value
    })

    const token = loginResponse.data.access_token

    // Store the token using your Axios plugin
    setAuthToken(token)

    // Decode the token to extract role and user_id
    const tokenData = parseJwt(token)

    // Update Vuex store with auth details
    store.commit('setAuth', { token, role: tokenData.role })

    // Show success message
    successMessage.value = 'Registration successful! Redirecting to dashboard...'

    // Redirect based on role after a short delay
    setTimeout(() => {
      redirectByRole(tokenData.role)
    }, 2000)
  } catch (error) {
    console.error('Registration or login failed:', error)
    if (error.response && error.response.data && error.response.data.detail) {
      errorMessage.value = error.response.data.detail
    } else {
      errorMessage.value = 'An unexpected error occurred. Please try again.'
    }
  } finally {
    isSubmitting.value = false
  }
}

// Function to decode JWT token
function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(function(c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
        })
        .join('')
    )
    return JSON.parse(jsonPayload)
  } catch (e) {
    console.error('Failed to parse JWT:', e)
    return {}
  }
}

// Function to redirect based on user role
function redirectByRole(role) {
  if (role === 'teacher') {
    location.href = '/teacher'
  } else if (role === 'parent' || role === 'class_rep') {
    location.href = '/parent'
  } else if (role === 'admin') {
    location.href = '/admin'
  } else {
    // Default redirect if role is unrecognized
    location.href = '/'
  }
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>

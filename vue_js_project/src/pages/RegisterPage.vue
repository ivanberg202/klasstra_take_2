<!-- filename: vue_js_project/src/pages/RegisterPage.vue -->
<template>
  <DefaultLayout>
    <div class="max-w-md mx-auto bg-white dark:bg-gray-800 p-6 rounded shadow">
      <h1 class="text-xl font-bold mb-4">Register</h1>
      <input v-model="username" placeholder="Username" class="w-full mb-2 p-2 border rounded"/>
      <input v-model="firstName" placeholder="First Name" class="w-full mb-2 p-2 border rounded"/>
      <input v-model="lastName" placeholder="Last Name" class="w-full mb-2 p-2 border rounded"/>
      <input v-model="email" placeholder="Email" class="w-full mb-2 p-2 border rounded"/>
      <input v-model="password" type="password" placeholder="Password" class="w-full mb-2 p-2 border rounded"/>
      <select v-model="role" class="w-full mb-4 p-2 border rounded">
        <option value="teacher">Teacher</option>
        <option value="parent">Parent</option>
      </select>
      <button @click="register" class="bg-primary text-white w-full p-2 rounded">Register</button>
    </div>
  </DefaultLayout>
</template>

<script setup>
import axios from 'axios'
import DefaultLayout from '../layouts/DefaultLayout.vue'
const username = ref('')
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const role = ref('parent')

async function register(){
  await axios.post('/users', {
    username: username.value,
    first_name: firstName.value,
    last_name: lastName.value,
    email: email.value,
    password: password.value,
    role: role.value
  })
  location.href='/login'
}
</script>

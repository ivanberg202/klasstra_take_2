<!-- filename: vue_js_project/src/pages/LoginPage.vue -->
<template>
  <DefaultLayout>
    <div class="max-w-md mx-auto bg-white dark:bg-gray-800 p-6 rounded shadow">
      <h1 class="text-xl font-bold mb-4">Login</h1>
      <input v-model="username" placeholder="Username or Email" class="w-full mb-2 p-2 border rounded"/>
      <input v-model="password" type="password" placeholder="Password" class="w-full mb-4 p-2 border rounded"/>
      <button @click="login" class="bg-primary text-white w-full p-2 rounded">Login</button>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { useStore } from 'vuex'
import axios from 'axios'
import DefaultLayout from '../layouts/DefaultLayout.vue'
const store = useStore()
const username = ref('')
const password = ref('')

async function login(){
  const res = await axios.post('/auth/login', { username: username.value, password: password.value })
  store.commit('setAuth', { token: res.data.access_token, role: parseJwt(res.data.access_token).role })
  redirectByRole()
}

function parseJwt (token) {
  const base64Url = token.split('.')[1]
  return JSON.parse(decodeURIComponent(atob(base64Url).split('').map(function(c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
  }).join('')))
}

function redirectByRole(){
  if(store.state.role === 'teacher') location.href='/teacher'
  else if(store.state.role === 'parent' || store.state.role === 'class_rep') location.href='/parent'
  else if(store.state.role === 'admin') location.href='/admin'
}
</script>

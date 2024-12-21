// filename: vue_js_project/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import './assets/tailwind.css'
import router from './router'
import store from './store'
import axios, { setAuthToken } from './plugins/axios' // Ensure axios is configured
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

const app = createApp(App)

app.use(router)
app.use(store)
app.use(Toast, {
  // You can set your default options here
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
})

app.mount('#app')

// Handle dark mode
import { watch } from 'vue'

watch(
  () => store.state.darkMode,
  (newVal) => {
    if (newVal) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  },
  { immediate: true }
)

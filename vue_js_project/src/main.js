// filename: vue_js_project/src/main.js
import { createApp, watch } from 'vue'
import App from './App.vue'
import './assets/tailwind.css'
import router from './router'
import store from './store'
import axios from 'axios'

// Set base URL to your FastAPI backend
axios.defaults.baseURL = 'http://localhost:8000'

const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')

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

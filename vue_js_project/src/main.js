// filename: vue_js_project/src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import './assets/tailwind.css';
import router from './router';
import store from './store';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';

// Create the Vue app
const app = createApp(App);

// Apply dark mode class based on the store's state
function applyDarkMode() {
  if (store.state.darkMode) {
    document.documentElement.classList.add('dark');
    document.documentElement.classList.remove('light'); // Optional
  } else {
    document.documentElement.classList.remove('dark');
    document.documentElement.classList.add('light'); // Optional
  }
}

// Call the function once during app initialization
applyDarkMode();

// Watch for Vuex mutations to handle dark mode toggling dynamically
store.subscribe((mutation) => {
  if (mutation.type === 'toggleDarkMode' || mutation.type === 'setDarkMode') {
    applyDarkMode();
  }
});

// Install plugins
app.use(router);
app.use(store);
app.use(Toast, {
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
});

// Mount the app
app.mount('#app');

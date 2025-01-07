// filename: vue_js_project/src/store/index.js
import { createStore } from 'vuex';

const store = createStore({
  state: {
    token: localStorage.getItem('accessToken') || null, // Rehydrate token from localStorage
    role: null,
    darkMode: localStorage.getItem('darkMode') === 'true', // Retrieve dark mode preference
  },
  mutations: {
    setAuth(state, { token, role }) {
      state.token = token;
      state.role = role;
      // Save token to localStorage for persistence
      localStorage.setItem('accessToken', token);
    },
    clearAuth(state) {
      state.token = null;
      state.role = null;
      // Remove token from localStorage
      localStorage.removeItem('accessToken');
    },
    toggleDarkMode(state) {
      state.darkMode = !state.darkMode;
      localStorage.setItem('darkMode', state.darkMode); // Save preference to localStorage
    },
    setDarkMode(state, value) {
      state.darkMode = value;
      localStorage.setItem('darkMode', value); // Save preference to localStorage
    },
  },
  actions: {
    login({ commit }, payload) {
      commit('setAuth', payload);
    },
    logout({ commit }) {
      commit('clearAuth');
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
    getUserRole: (state) => state.role,
  },
});

export default store;

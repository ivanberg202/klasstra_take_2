// filename: src/store/index.js
import { createStore } from 'vuex';
import jwt_decode from 'jwt-decode'; // Install this package for decoding JWT

const store = createStore({
  state: {
    token: localStorage.getItem('accessToken') || null, // Rehydrate token from localStorage
    role: localStorage.getItem('userRole') || null,     // Rehydrate role from localStorage
    darkMode: localStorage.getItem('darkMode') === 'true', // Retrieve dark mode preference
    tokenData: null, // Store decoded token data
  },
  mutations: {
    setAuth(state, { token, role }) {
      state.token = token;
      state.role = role;

      // Save token and role in localStorage
      localStorage.setItem('accessToken', token);
      localStorage.setItem('userRole', role);

      // Decode token and store data
      try {
        state.tokenData = jwt_decode(token);
      } catch (e) {
        state.tokenData = null;
      }
    },
    clearAuth(state) {
      state.token = null;
      state.role = null;
      state.tokenData = null;

      // Remove token and role from localStorage
      localStorage.removeItem('accessToken');
      localStorage.removeItem('userRole');
    },
    toggleDarkMode(state) {
      state.darkMode = !state.darkMode;
      localStorage.setItem('darkMode', state.darkMode); // Save preference to localStorage
    },
    setDarkMode(state, value) {
      state.darkMode = value;
      localStorage.setItem('darkMode', value); // Save preference to localStorage
    },
    rehydrateAuth(state) {
      const storedToken = localStorage.getItem('accessToken');
      const storedRole = localStorage.getItem('userRole');

      if (storedToken && storedRole) {
        state.token = storedToken;
        state.role = storedRole;

        // Decode the token to extract additional data
        try {
          state.tokenData = jwt_decode(storedToken);
        } catch (e) {
          state.tokenData = null;
        }
      } else {
        state.token = null;
        state.role = null;
        state.tokenData = null;
      }
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
    getUserId: (state) => state.tokenData?.user_id,
  },
});

export default store;

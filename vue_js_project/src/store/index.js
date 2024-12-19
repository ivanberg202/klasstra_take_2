// filename: vue_js_project/src/store/index.js
import { createStore } from 'vuex'

export default createStore({
  state: {
    token: null,
    role: null,
    darkMode: false,
  },
  mutations: {
    setAuth(state, { token, role }) {
      state.token = token
      state.role = role
    },
    toggleDarkMode(state) {
      state.darkMode = !state.darkMode
    }
  },
  actions: {},
  getters: {}
})

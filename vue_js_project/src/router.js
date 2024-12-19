// filename: vue_js_project/src/router.js
import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from './pages/LoginPage.vue'
import RegisterPage from './pages/RegisterPage.vue'
import DashboardTeacher from './pages/DashboardTeacher.vue'
import DashboardParent from './pages/DashboardParent.vue'
import DashboardAdmin from './pages/DashboardAdmin.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/teacher', component: DashboardTeacher },
  { path: '/parent', component: DashboardParent },
  { path: '/admin', component: DashboardAdmin }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

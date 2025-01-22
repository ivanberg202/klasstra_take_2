// filename: src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from './pages/LoginPage.vue';
import RegisterPage from './pages/RegisterPage.vue';
import DashboardTeacher from './pages/DashboardTeacher.vue';
import DashboardParent from './pages/DashboardParent.vue';
import DashboardAdmin from './pages/DashboardAdmin.vue';
import store from './store/index.js'; // Import the store for route guards
import AiAssistantPage from './pages/AiAssistantPage.vue'; // import


const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { 
    path: '/teacher', 
    component: DashboardTeacher,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  { 
    path: '/parent', 
    component: DashboardParent,
    meta: { requiresAuth: true, role: ['parent', 'class_rep'] }
  },
  { 
    path: '/admin', 
    component: DashboardAdmin,
    meta: { requiresAuth: true, role: 'admin' }
  },
  // Add a catch-all route for 404
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('./pages/NotFound.vue') },
  { 
    path: '/ai-assistant', 
    component: AiAssistantPage,
    meta: { requiresAuth: true, role: ['teacher', 'admin', 'class_rep'] } 
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Global navigation guard
router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth;
  const role = to.meta.role;
  const isAuthenticated = store.getters.isAuthenticated;
  const userRole = store.getters.getUserRole;

  if (requiresAuth) {
    if (!isAuthenticated) {
      return next('/login');
    }

    if (role) {
      if (Array.isArray(role)) {
        if (!role.includes(userRole)) {
          return next('/login');
        }
      } else {
        if (userRole !== role) {
          return next('/login');
        }
      }
    }
  }

  next();
});

export default router;

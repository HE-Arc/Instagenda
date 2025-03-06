import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import axios from 'axios'
import RegisterView from '@/views/RegisterView.vue'
import { useAuth } from '@/components/useAuth'

const { user } = useAuth();

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {requiresGuest: true}
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: {requiresGuest: true}
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/user',
      name: 'user',
      component: () => import('../views/UserView.vue'),
      meta: {requiresAuth: true}
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {requiresAuth: true}
    },
    {
      path: '/groups/:id',
      name: 'group-detail',
      component: () => import('../views/GroupDetailView.vue'),
      meta: { requiresAuth: true }
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    try {
      const response = await axios.get('/profile');
      if (response.status === 200) {
        user.value = response.data;
        next();
      } else {
        user.value = null;
        next('/login');
      }
    } catch (error) {
      next('/login');
    }
  } else if (to.meta.requiresGuest) {
    try {
      const response = await axios.get('/profile');
      if (response.status === 200) {
        next('/');
      } else {
        next();
      }
    } catch (error) {
      next();
    }
  } else {
    next();
  }
})

export default router

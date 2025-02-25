import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import axios from 'axios'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
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
    }
  ],
})

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    try {
      const response = await axios.get('/profile');
      if (response.status === 200) {
        next();
      } else {
        next('/');
      }
    } catch (error) {
      next('/');
    }
  } else if (to.meta.requiresGuest) {
    try {
      const response = await axios.get('/profile');
      if (response.status === 200) {
        next('/user');
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

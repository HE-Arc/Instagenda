import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'
import { useAuth } from '@/components/store'

const { user } = useAuth();

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: {requiresGuest: true}
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
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
      component: () => import('../views/HomeView.vue'),
      meta: {requiresAuth: true}
    },
    {
      path: '/groups/:id',
      name: 'group-detail',
      component: () => import('../views/GroupDetailView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/ig-connection',
      name: 'ig-connection',
      component: () => import('../views/IGConnectionView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/create-post/:id',
      name: 'create-post',
      component: () => import('../views/CreatePostView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/update-post/:id',
      name: 'update-post',
      component: () => import('../views/UpdatePostView.vue'),
      meta: { requiresAuth: true }
    }
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

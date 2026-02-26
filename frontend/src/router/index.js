import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomePage.vue')
  },
  {
    path: '/category/:id',
    name: 'Category',
    component: () => import('../views/CategoryPage.vue')
  },
  {
    path: '/post/:id',
    name: 'PostDetail',
    component: () => import('../views/PostDetailPage.vue')
  },
  {
    path: '/create',
    name: 'CreatePost',
    component: () => import('../views/CreatePostPage.vue')
  },
  {
    path: '/admin/review',
    name: 'AdminReview',
    component: () => import('../views/AdminReviewPage.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginPage.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterPage.vue')
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: () => import('../views/NotificationPage.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

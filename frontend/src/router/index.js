import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/Login.vue';
import HomeView from '../views/Home.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    meta: { requiresAuth: true }, // 需要登录的路由
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 路由守卫，判断是否需要登录
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token'); // 假设你将 token 存储在 localStorage 中
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'Login' }); // 未登录，跳转到登录页面
  } else {
    next();
  }
});

export default router;

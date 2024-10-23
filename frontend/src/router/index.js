import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/Login.vue';
import HomeView from '../views/Home.vue';
import RegisterView from '../views/Register.vue';
import UserAccountView from "../views/UserAccount.vue";
import ModifyPasswordView from "../views/ModifyPassword.vue";
import ModifyInfoView from "../views/ModifyInfo.vue";
import InformationView from "../views/Information.vue";

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
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
  },
  {
    path: '/account',
    name: 'UserAccount',
    component: UserAccountView,
  },
  {
    path: '/modifypassword',
    name: 'ModifyPassword',
    component: ModifyPasswordView,
  },
  {
    path: '/modifyinfo',
    name: 'ModifyInfo',
    component: ModifyInfoView,
  },
  {
    path: '/information',
    name: 'Information',
    component: InformationView,
  }
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

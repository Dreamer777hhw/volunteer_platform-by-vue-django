import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/Login.vue';
import HomeView from '../views/Home.vue';
import RegisterView from '../views/Register.vue';
import UserAccountView from "../views/UserAccount.vue";
import ModifyPasswordView from "../views/ModifyPassword.vue";
import ModifyInfoView from "../views/ModifyInfo.vue";
import InformationView from "../views/Information.vue";
import CreateActivityView from "../views/CreateActivity.vue";
import ReviseActivityView from "../views/ReviseActivity.vue"; // 新增导入

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
  },
  {
    path: '/activity/create',
    name: 'CreateActivity',
    component: CreateActivityView,
  },
  {
    path: '/activity/revise/:activity_id_hash',
    name: 'ReviseActivity',
    component: ReviseActivityView,
    props: true, // 传递路由参数作为组件的 props
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
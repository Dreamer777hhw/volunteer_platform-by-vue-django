<template>
  <div>
    <h1>登录</h1>
    <form @submit.prevent="login">
      <input type="email" v-model="email" placeholder="邮箱" required />
      <input type="password" v-model="password" placeholder="密码" required />
      <button type="submit">登录</button>
      <p>还没有账户？ <router-link to="/register">注册</router-link></p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/api/login', { email: this.email, password: this.password });
        localStorage.setItem('token', response.data.token); // 假设后端返回 token
        this.$router.push('/');
      } catch (error) {
        console.error('登录失败', error);
      }
    },
  },
};
</script>

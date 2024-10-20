<template>
  <div>
    <h1>欢迎来到志愿者管理系统</h1>
    <button @click="logout">注销</button>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  methods: {
    logout() {
      localStorage.removeItem('token'); // 清除 token
      this.$router.push('/login'); // 跳转到登录页面
    },
  },
};
</script>


// Attention: Without backend
// TODO1 : beatify the login page
// TODO2 : add the login logic

<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="login-title">登录</h2>
      <div class="user-type-selector">
        <button @click="selectUserType('volunteer')" :class="{ active: userType === 'volunteer' }">我是志愿者</button>
        <button @click="selectUserType('organizer')" :class="{ active: userType === 'organizer' }">我是发布者</button>
      </div>
      <div class="input-group">
        <input
          type="text"
          v-model="username"
          placeholder="账号"
          required
        />
        <input
          type="password"
          v-model="password"
          placeholder="密码"
          required
        />
        
      </div>
      <div class="remember-me">
        <input type="checkbox" v-model="rememberMe" />
        <label>记住密码</label>
      </div>
      <div class="actions">
        <button class="login-button" @click="login">确认登录</button>
        <router-link to="/register" class="register-link">注册</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name : 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false,
      userType: 'volunteer', // 默认选择为志愿者
    };
  },
  methods: {
    selectUserType(type) {
      this.userType = type;
    },
    login() {
      if (this.username === 'root' && this.password === 'passwd') {
        // 登录成功的逻辑
        console.log('登录成功');
        this.$router.push('/'); // 跳转到首页
      } else {
        // 登录失败的逻辑
        alert('账号或密码错误');
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 300px;
}

.login-title {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.user-type-selector {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.user-type-selector button {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 0 0.5rem;
  transition: background-color 0.3s;
}

.user-type-selector button.active {
  background-color: #007bff;
  color: white;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group input {
  margin-bottom: 1rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.remember-me {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.actions {
  display: flex;
  justify-content: space-between;
}

.login-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.register-link {
  color: #007bff;
  text-decoration: none;
}
</style>

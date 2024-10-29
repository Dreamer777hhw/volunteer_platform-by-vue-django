<!-- 
    * @FileDescription: 登录页面组件，包含用户类型选择、账号密码输入、记住密码功能
    * @Author: infinity 
    * @Date: 2024-10-29 
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-29
 -->

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
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
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
import axios from 'axios';
import "./../assets/css/common.css";
export default {
  name : 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false,
      userType: 'volunteer', // 默认选择为志愿者
      errorMessage: '', 
    };
  },
  created() {
    this.username = localStorage.getItem('username');
    if (localStorage.getItem('rememberMe') === 'true') {
      this.password = localStorage.getItem('password');
    }
    this.AutoTokenLogin();
    this.AutoPasswdLogin();
  },
  methods: {
    /**
     * @description 选择用户类型
     * @param {string} type 用户类型（'volunteer' 或 'organizer'）
     * @return {void}
     */
    selectUserType(type) {
      this.userType = type;
    },
    /**
     * @description 登录方法，验证用户名和密码，并处理记住密码逻辑
     * @return {void}
     */
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/login/', {
          user_id: this.username,
          password: this.password,
          user_type: this.userType,
        });

        // 登录成功处理
        if (response.status === 200) {
          const token = response.data.token;
          localStorage.setItem('token', token);
          // alert('登录成功！');
          localStorage.setItem('username', this.username);

          if (this.rememberMe) {
            localStorage.setItem('password', this.password);
            localStorage.setItem('rememberMe', 'True');
          } else {
            localStorage.removeItem('password');
            localStorage.removeItem('rememberMe');
          }

          this.$router.push({ path: '/' }); // 跳转到首页
        }
      } catch (error) {
        // 处理错误
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.error + ", 请重试";
        } else {
          this.errorMessage = "网络错误，请重试";
        }
      }
    },
    /**
     * @description 自动使用 token 登录
     * @return {void}
     */
    async AutoTokenLogin() {
      const token = localStorage.getItem('token');

      if (token) {
        try {
          const response = await axios.post('http://127.0.0.1:8000/api/autotokenlogin/', {
            token: token,
          });

          // 登录成功处理
          if (response.status === 200) {
            // alert('自动登录成功！');
            this.$router.push({ path: '/' }); // 跳转到首页
          }
        } catch (error) {
          // 处理错误
          if (error.response && error.response.data) {
            alert("自动登录失败: " + JSON.stringify(error.response.data));
          } else {
            alert("自动登录失败: 网络错误");
          }
        }
      } else {
        // alert("未找到 token，请手动登录。");
      }
    },
    /**
     * @description 自动使用用户名和密码登录
     * @return {void}
     */
    async AutoPasswdLogin() {
      const userId = localStorage.getItem('user_id');
      const password = localStorage.getItem('password');
      const userType = this.userType;

      if (userId && password) {
        try {
          const response = await axios.post('http://127.0.0.1:8000/api/autopasswdlogin/', {
            user_id: userId,
            password: password,
            user_type: userType,
          });

          // 登录成功处理
          if (response.status === 200) {
            alert('凭据自动登录成功！');
            this.$router.push({ path: '/' }); // 跳转到首页
          }
        } catch (error) {
          // 处理错误
          if (error.response && error.response.data) {
            alert("凭据自动登录失败: " + JSON.stringify(error.response.data));
          } else {
            alert("凭据自动登录失败: 网络错误");
          }
        }
      } else {
        // alert("未找到用户凭据，请手动登录。");
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
  background-image: url('../../public/background/background1.jpg');
  background-size: cover;
  background-position: center;
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
  margin-bottom: 2rem;
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

.error-message {
  color: red;
  font-size: 0.875rem;
  margin-top: -0.5rem;
  margin-bottom: 1rem;
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
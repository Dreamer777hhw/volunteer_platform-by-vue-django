<!--
    * @FileDescription: 修改密码页面组件，包含新密码、确认新密码输入框，并进行相应的验证
    * @Author: Dreamer777hhw
    * @Date: 2024-10-23
    * @LastEditors: infinity
    * @LastEditTime: 2024-10-23
    *

    Attention: Without backend

    TODO:
        1. 前端页面美化
        2. 链接后端

 -->
<template>
<div>
  <NavBar />
  <div class="modify-password-container">
    <div class="password-card">
      <h2 class="password-title">修改密码</h2>
      <div class="info-item">
        <span class="info-label">旧密码：</span>
        <input v-model="oldPassword" type="password" placeholder="请输入旧密码" />
      </div>
      <div class="info-item">
        <span class="info-label">新密码：</span>
        <input v-model="newPassword" type="password" placeholder="请输入新密码" />
      </div>
      <div class="info-item">
        <span class="info-label">确认新密码：</span>
        <input v-model="confirmPassword" type="password" placeholder="请确认新密码" />
      </div>
      <button @click="submitPasswordChange">提交</button>
      <p v-if="passwordError" class="error-message">{{ passwordError }}</p>
    </div>
  </div>
</div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';

export default {
  name: 'ModifyPasswordView',
  components: {
    NavBar,
  },
  data() {
    return {
      oldPassword: '',
      newPassword: '',
      confirmPassword: '',
      passwordError: '',
    };
  },
  methods: {
    /**
     * @description 提交密码修改请求
     * @return {void}
     */
    async submitPasswordChange() {
      if (this.newPassword !== this.confirmPassword) {
        this.passwordError = '两次输入的密码不一致！';
        return;
      }

      if (this.newPassword.length < 6) {
        this.passwordError = '密码长度不能少于6个字符';
        return;
      }

      const token = localStorage.getItem('token'); // 从本地存储获取token
      if (!token) {
        this.passwordError = '未找到用户信息，请重新登录';
        return;
      }

      try {
        const response = await axios.post(
          `http://127.0.0.1:8000/api/changepasswd/`,
          { new_password: this.newPassword,
                  old_password: this.oldPassword,
                  token: token },
          {
            headers: {
              Authorization: `Bearer ${token}`, // 使用Token进行认证
            },
          }
        );

        if (response.status === 200) {
          alert('密码修改成功！');
          this.$router.push('/account'); // 修改成功后返回主页
        }
      } catch (error) {
        this.passwordError = '密码修改失败，请稍后重试';
        console.error("修改密码时发生错误:", error);
      }
    },
  },
};
</script>

<style scoped>
.modify-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90vh;
  background-color: #f0f2f5;
  padding: 2rem;
}

.password-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 300px;
}

.password-title {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.info-item {
  margin-bottom: 1rem;
}

.error-message {
  color: red;
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

button {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>

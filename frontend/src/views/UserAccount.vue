<!--
    * @FileDescription: 个人账户页面组件，包含学号、姓名、学院、专业、邮箱、手机号、密码等信息展示，以及修改信息、修改密码、注销账户等功能
    * @Author: Dreamer777hhw
    * @Date: 2024-10-22
    * @LastEditors: infinity
    * @LastEditTime: 2024-10-23
    *

    Attention: Without backend

    TODO:
        1. 前端页面美化
        2. 连接后端

 -->
<template>
<div>
  <NavBar/>
  <div class="account-container">
    <div class="account-card">
      <h2 class="account-title">个人账户</h2>
      <div v-if="isEditingInfo" class="info-edit">
        <div class="info-item">
          <span class="info-label">姓名：</span>
          <input v-model="editName" type="text" />
        </div>
        <div class="info-item">
          <span class="info-label">学院：</span>
          <input v-model="editSchool" type="text" />
        </div>
        <div class="info-item">
          <span class="info-label">专业：</span>
          <input v-model="editMajor" type="text" />
        </div>
        <div class="info-item">
          <span class="info-label">邮箱：</span>
          <input v-model="editEmail" type="email" />
        </div>
        <div class="info-item">
          <span class="info-label">手机号：</span>
          <input v-model="editPhone" type="text" />
        </div>
        <button @click="submitInfoChange">提交修改</button>
      </div>

      <div v-else>
        <div class="account-info">
          <div class="info-item">
            <span class="info-label account-label">学号：</span>
            <span class="info-value">{{ studentId }}</span>
          </div>
          <div class="info-item">
            <span class="info-label account-label">姓名：</span>
            <span class="info-value">{{ name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label account-label">学院：</span>
            <span class="info-value">{{ school }}</span>
          </div>
          <div class="info-item">
            <span class="info-label account-label">专业：</span>
            <span class="info-value">{{ major }}</span>
          </div>
          <div class="info-item">
            <span class="info-label account-label">邮箱：</span>
            <span class="info-value">{{ email }}</span>
          </div>
          <div class="info-item">
            <span class="info-label account-label">手机号：</span>
            <span class="info-value">{{ phone }}</span>
          </div>
          <div class="info-item">
            <span class="info-label account-label">密码：</span>
            <span class="info-value">{{ '*'.repeat(password.length) }}</span>
          </div>
        </div>
      </div>
    </div>

    <button class="change-password-button" @click="goToModifyPassword">修改密码</button>
    <button class='change-password-button' @click="goToModifyInfo">修改信息</button>
    <button @click="logout" class="logout-button">注销账户</button>
  </div>
</div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
export default {
  name: 'UserAccountView',
  components: {
    NavBar,
  },
  data() {
    return {
      studentId: '123456',
      name: '张三',
      school: '计算机学院',
      major: '软件工程',
      email: 'zhangsan@example.com',
      phone: '13800000000',
      password: '123456',
      isEditingInfo: false, // 是否正在修改信息
      isEditingPassword: false, // 是否正在修改密码
      editName: '',
      editSchool: '',
      editMajor: '',
      editEmail: '',
      editPhone: '',
      newPassword: '',
      confirmPassword: '',
      passwordError: '',
    };
  },
  methods: {
    /**
     * @description 信息修改
     * @return {void}
     */
    goToModifyInfo() {
      this.$router.push({
        path: '/modifyinfo',
        query: {
          name: this.name,
          school: this.school,
          major: this.major,
          email: this.email,
          phone: this.phone,
        },
      }); // Navigate to the modify info page with user data
    },
    /**
     * @description 密码修改
     * @return {void}
     */
    goToModifyPassword() {
      this.$router.push('/modifypassword'); // Navigate to the modify password page
    },
    /**
     * @description 返回主页
     * @return {void}
     */
    logout() {
      // 处理注销账户逻辑
      localStorage.removeItem('token');
      alert('注销成功，正在返回主页...');
      this.$router.push('/'); // 返回主页
    }
  }
};
</script>

<style scoped>
.account-container {
  padding-top: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f0f2f5;
  height: 85vh;
}

.account-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 300px;
  margin-bottom: 1rem;
}

.password-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 300px;
}

.account-title,
.password-title {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.account-info {
  display: flex;
  flex-direction: column;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.info-edit {
  margin-bottom: 1rem;
}

.input-field input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.change-password-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 0.2rem 0.5rem;
  cursor: pointer;
  margin-left: 10px;
  width: 25%;
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

.logout-button {
  width: 25%;
  margin-top: 1rem;
  background-color: #dc3545;
}
</style>

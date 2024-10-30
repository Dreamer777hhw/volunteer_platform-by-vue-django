<!--
    * @FileDescription: 个人账户页面组件，包含学号、姓名、学院、专业、邮箱、手机号、密码等信息展示，以及修改信息、修改密码、注销账户等功能
    * @Author: Dreamer777hhw
    * @Date: 2024-10-22
    * @LastEditors: dreamer777hhw
    * @LastEditTime: 2024-10-30
    *

    Attention: Without backend

    TODO:
        1. 前端页面美化
        2. organize的界面要重新设计

 -->
<template>
<div>
  <NavBar />
  <div class="account-container">
    <div class="account-card">
      <h2 class="account-title">个人账户</h2>
      <div v-if="userType === 'volunteer'">
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
<!--          <div class="info-item">-->
<!--            <span class="info-label account-label">密码：</span>-->
<!--            <span class="info-value">{{ '*'.repeat(password.length) }}</span>-->
<!--          </div>-->
        </div>
      </div>
      <div v-else-if="userType === 'organizer'">
        <div class="info-item">
          <span class="info-label account-label">姓名：</span>
          <span class="info-value">{{ organizerName }}</span>
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
import axios from 'axios';
export default {
  name: 'AccountView',
  components: {
    NavBar,
  },
  data() {
    return {
      studentId: '',
      name: '',
      school: '',
      major: '',
      email: '',
      phone: '',
      password: '',
      organizerName: '',
      userType: '',
    };
  },
  mounted() {
    this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error("未找到token");
        return;
      }

      this.userType = localStorage.getItem('user_type');
      if (this.userType === 'volunteer') {
        try {
          const response = await axios.get(`http://127.0.0.1:8000/api/account/${token}/`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          const data = response.data;
          this.studentId = data.student_id;
          this.name = data.name;
          this.school = data.school;
          this.major = data.major;
          this.email = data.email;
          this.phone = data.phone;
          this.password = ''; // 这里你可以决定是否要显示密码
        } catch (error) {
          console.error("获取用户数据失败:", error);
        }
      } else if (this.userType === 'organizer') {
        this.organizerName = localStorage.getItem('name'); // 从localStorage获取组织者的姓名
      }
    },
    goToModifyInfo() {
      this.$router.push('/modifyinfo'); // 跳转到修改信息页面
    },
    goToModifyPassword() {
      this.$router.push('/modifypassword'); // 跳转到修改密码页面
    },
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('user_type');
      alert('注销成功，正在返回主页...');
      this.$router.push('/'); // 返回主页
    }
  },
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
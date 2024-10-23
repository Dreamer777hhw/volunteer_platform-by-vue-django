<template>
  <div class="modify-password-container">
    <div class="password-card">
      <h2 class="password-title">修改密码</h2>
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
</template>

<script>
export default {
  name: 'ModifyPasswordView',
  data() {
    return {
      newPassword: '',
      confirmPassword: '',
      passwordError: '',
    };
  },
  methods: {
    submitPasswordChange() {
      if (this.newPassword !== this.confirmPassword) {
        this.passwordError = '两次输入的密码不一致！';
        return;
      }

      if (this.newPassword.length < 6) {
        this.passwordError = '密码长度不能少于6个字符';
        return;
      }

      // 处理密码修改逻辑
      alert('密码修改成功！');
      this.$router.push('/home'); // 修改成功后返回主页
    },
  },
};
</script>

<style scoped>
.modify-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
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

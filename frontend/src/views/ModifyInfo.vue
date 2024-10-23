<template>
  <div class="modify-info-container">
    <div class="info-card">
      <h2>修改信息</h2>
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
        <select v-model="editMajor">
          <option value="软件工程">软件工程</option>
          <option value="计算机科学">计算机科学</option>
          <option value="信息技术">信息技术</option>
          <!-- Add more options as needed -->
        </select>
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
  </div>
</template>

<script>
export default {
  name: 'ModifyInfoView',
  data() {
    return {
      editName: this.$route.query.name || '',
      editSchool: this.$route.query.school || '',
      editMajor: this.$route.query.major || '',
      editEmail: this.$route.query.email || '',
      editPhone: this.$route.query.phone || '',
    };
  },
  methods: {
    submitInfoChange() {
      // Logic to submit modified info
      alert('信息修改成功！');
      this.$router.push('/useraccount'); // Navigate back to the account page
    }
  }
};
</script>

<style scoped>
.modify-info-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
  padding: 2rem;
}

.info-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 300px;
}

.info-item {
  margin-bottom: 1rem;
}
</style>

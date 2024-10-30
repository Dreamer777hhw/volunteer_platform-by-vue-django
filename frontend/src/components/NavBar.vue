<!-- 
    * @FileDescription: 导航栏组件，包含首页、我的活动和账户信息的导航功能
    * @Author: infinity 
    * @Date: 2024-10-21 
    * @LastEditors: infinity
    * @LastEditTime: 2024-10-21
 -->

<template>
  <nav class="navbar">
    <div class="navbar-content">
      <div class="navbar-title" @click="goHome">第三课堂</div>
      <div class="navbar-right">
        <div class="navbar-item" @click="goToInformation">我的活动</div>
        <div class="navbar-item username-item" @click="goToAccount">{{ username }}</div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      username: localStorage.getItem('name')
    };
  },
  methods: {
    /**
     * @description 跳转到首页
     * @return {void}
     */
    goHome() {
      this.$router.push('/');
    },
    /**
     * @description 跳转到我的活动页面
     * @return {void}
     */
    goToInformation() {
      this.$router.push('/information');
    },
    /**
     * @description 跳转到账户信息页面
     * @return {void}
     */
    goToAccount() {
      this.$router.push('/account');
    },
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ff6600; /* 导航栏背景颜色 */
  padding: 1rem 2rem;
  color: white;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  border-top-left-radius: 10px; /* 上部分圆角 */
  border-top-right-radius: 10px; /* 上部分圆角 */
}

.navbar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.navbar-title {
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
}

.navbar-right {
  margin-right: 2rem;
  display: flex;
  gap: 2rem;
}

.navbar-item {
  margin-right: 2rem;
  font-size: 1.2rem;
  cursor: pointer;
}

</style>
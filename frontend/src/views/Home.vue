<!--
    * @FileDescription: 首页视图组件，包含导航栏，轮播图，推荐列表，活动视图
    * @Author: infinity
    * @Date: 2024-10-22
    * @LastEditors: dreamer777hhw
    * @LastEditTime: 2024-10-31
 -->

<template>
  <div>
    <NavBar />
    <div class="home-container">
      <div class="content-wrapper">
        <BannerComponent />
        <RecommendComponent />
        <ActivityListComponent />
      </div>
      <button class="scroll-to-top" @click="scrollToTop" v-if="isVisible">
        <i class="fas fa-arrow-up"></i> <!-- Font Awesome 上的向上箭头图标 -->
      </button>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import BannerComponent from '@/components/Banner.vue';
import RecommendComponent from '@/components/Recommend.vue';
import ActivityListComponent from '@/components/ActivityList.vue';
import axios from 'axios';

export default {
  name: 'HomeView',
  components: {
    NavBar,
    BannerComponent,
    RecommendComponent,
    ActivityListComponent,
  },
  data() {
    return {
      isVisible: false, // 控制按钮显示状态
    };
  },
  async mounted() {
    await this.updateActivityStatus();
    window.addEventListener('scroll', this.handleScroll); // 监听滚动事件
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll); // 清理事件监听
  },
  methods: {
    async updateActivityStatus() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/update-status/');
        console.log('活动状态更新成功:', response.data);
      } catch (error) {
        console.error('更新活动状态失败:', error);
      }
    },
    handleScroll() {
      this.isVisible = window.scrollY > 300; // 超过300px时显示按钮
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' }); // 平滑滚动到顶部
    },
  },
};
</script>

<style scoped>
.home-container {
  padding-top: 80px; /* 给内容留出导航栏的高度 */
  display: flex;
  justify-content: center;
  background-image: url('../../public/background/bg.webp');
  background-repeat: repeat;
  background-size: auto;
  background-position: center;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 1200px;
  max-width: 100%;
}

.content-wrapper > * {
  width: 100%;
  margin-bottom: 20px; /* 组件之间的间距 */
}

.scroll-to-top {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: rgba(0, 123, 255, 0.7);
  color: white;
  border: none;
  border-radius: 50%; /* 使按钮为圆形 */
  width: 50px; /* 按钮宽度 */
  height: 50px; /* 按钮高度 */
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0.8;
  transition: opacity 0.3s;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2); /* 阴影效果 */
}

.scroll-to-top:hover {
  opacity: 1;
}

.scroll-to-top i {
  font-size: 20px; /* 图标大小 */
}

/* 在小屏幕上可能需要调整按钮位置 */
@media (max-width: 600px) {
  .scroll-to-top {
    bottom: 15px;
    right: 15px;
    width: 40px; /* 调整宽度 */
    height: 40px; /* 调整高度 */
  }
}
</style>
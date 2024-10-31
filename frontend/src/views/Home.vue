<!-- 
    * @FileDescription: 首页视图组件，包含导航栏，轮播图，推荐列表，活动视图
    * @Author: infinity
    * @Date: 2024-10-22 
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-22 
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
  async mounted() {
    await this.updateActivityStatus();
  },
  methods: {
    async updateActivityStatus() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/update-status/');
        console.log('活动状态更新成功:', response.data);
        // 可以在这里处理更新后的状态，比如将其存储到 Vuex 或组件的状态中
      } catch (error) {
        console.error('更新活动状态失败:', error);
      }
    },
  },
};
</script>

<style scoped>
.home-container {
  padding-top: 80px; /* 给内容留出导航栏的高度 */
  display: flex;
  justify-content: center;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 1200px; 
  max-width: 100%; 
  /* margin: 0 auto; */
}

.content-wrapper > * {
  width: 100%;
  margin-bottom: 20px; /* 组件之间的间距 */
}

/* @media (max-width: 1200px) {
  .content-wrapper {
    padding: 0 20px; 
  }
}

@media (max-width: 1240px) {
  .home-container {
    overflow-x: auto; 
  }
} */
</style>
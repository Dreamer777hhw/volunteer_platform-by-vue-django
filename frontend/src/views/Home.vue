<!-- 
    * @FileDescription: 首页视图组件，包含导航栏，轮播图，推荐列表，活动视图
    * @Author: infinity
    * @Date: 2024-10-22 
    * @LastEditors: infinity 
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
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import BannerComponent from '@/components/Banner.vue';
import RecommendComponent from '@/components/Recommend.vue';
import ActivityListComponent from '@/components/ActivityList.vue';

export default {
  name: 'HomeView',
  components: {
    NavBar,
    BannerComponent,
    RecommendComponent,
    ActivityListComponent,
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
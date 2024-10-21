<!-- 
    * @FileDescription: 首页视图组件，包含导航栏，轮播图，推荐列表，活动视图
    * @Author: infinity
    * @Date: 2024-10-21 
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-21 
 -->

<template>
  <div>
    <NavBar />
    <div class="home-container">
      <BannerComponent />
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';  
import BannerComponent from '@/components/Banner.vue';

export default {
  name: 'HomeView',
  components: {
    NavBar,
    BannerComponent,
  },
};
</script>

<style scoped>
.home-container {
  padding-top: 80px; /* 给内容留出导航栏的高度 */
}
</style>

<!-- 
    * @FileDescription: 推荐活动组件，包含猜你喜欢和热门活动两个标签页，以及活动卡片列表
    * @Author: infinity 
    * @Date: 2024-10-22 
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-22 
 -->

<template>
  <div class="recommend-container">
    <div class="recommend-section">
      <div class="recommend-header">
        <div class="buttons">
          <button :class="{'active': currentTab === 'recommend'}" @click="fetchActivities('recommend')">猜你喜欢</button>
          <button :class="{'active': currentTab === 'hot'}" @click="fetchActivities('hot')">热门活动</button>
        </div>
      </div>

      <!-- 活动卡片列表 -->
      <ActivityCardRow :activities="filteredActivities" />
    </div>
  </div>
</template>

<script>
import ActivityCardRow from '@/components/ActivityCardRow.vue';
import axios from 'axios';

export default {
  name: 'RecommendComponent',
  components: {
    ActivityCardRow,
  },
  data() {
    return {
      currentTab: 'recommend', // 默认显示“猜你喜欢”标签页
      activities: [],
    };
  },
  computed: {
    filteredActivities() {
      return this.activities; // 返回获取到的活动数据
    },
  },
  methods: {
    async fetchActivities(tab) {
      try {
        this.currentTab = tab; // 更新当前标签
        const username = localStorage.getItem('username'); // 从 localStorage 获取用户名
        const response = await axios.get(`http://127.0.0.1:8000/api/recommend/${tab}/${username}`); // 将用户名添加到请求中
        this.activities = response.data; // 更新活动数据
        console.log('当前用户:', username); // 打印用户名，你可以根据需求使用
      } catch (error) {
        console.error('获取活动失败:', error);
      }
    },
  },
  mounted() {
    this.fetchActivities(this.currentTab); // 初始化时加载活动
  },
};
</script>

<!-- 
    * @FileDescription: 推荐活动组件，包含猜你喜欢和热门活动两个标签页，以及活动卡片列表
    * @Author: infinity 
    * @Date: 2024-10-21 
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-21 
 -->

<template>
  <div class="recommend-section">
    <div class="recommend-header">
      <div class="buttons">
        <button :class="{'active': currentTab === 'recommend'}" @click="currentTab = 'recommend'">猜你喜欢</button>
        <button :class="{'active': currentTab === 'hot'}" @click="currentTab = 'hot'">热门活动</button>
      </div>
      <button class="refresh-button" @click="refreshItems">刷新</button>
    </div>

    <!-- 活动卡片列表 -->
    <div class="activity-cards">
      <ActivityCard 
        v-for="(activity, index) in activities" 
        :key="index" 
        :activity="activity"
      />
    </div>
  </div>
</template>

<script>
import ActivityCard from '@/components/ActivityCard.vue';

export default {
  name: 'RecommendComponent',
  components: {
    ActivityCard,
  },
  data() {
    return {
      currentTab: 'recommend', // 默认显示“猜你喜欢”标签页
      activities: [
        // 假设的静态活动数据
        // TODO 从后端获取真实数据
        {
          image: 'activity-images/activity-1.jpg',
          title: '旋律欣赏活动1',
          host: '艺术学院',
          participants: '60 / 60 人',
          registrationPeriod: '2024-10-12 ~ 2024-10-23',
          location: '图书馆',
          activityPeriod: '2024-10-10 ~ 2024-10-21',
        },
        {
          image: 'activity-images/activity-1.jpg',
          title: '旋律欣赏活动2',
          host: '艺术学院',
          participants: '60 / 60 人',
          registrationPeriod: '2024-10-12 ~ 2024-10-23',
          location: '图书馆',
          activityPeriod: '2024-10-10 ~ 2024-10-21',
        },
        {
          image: 'activity-images/activity-2.jpg',
          title: '志愿招募活动',
          host: '志愿者组织',
          participants: '20 / 20 人',
          registrationPeriod: '2024-10-10 ~ 2024-10-14',
          location: '创新中心',
          activityPeriod: '2024-10-11 ~ 2024-10-15',
        },
      ],
    };
  },
  methods: {
    /**
     * @description 刷新活动列表
     * @return {void}
     */
    refreshItems() {
      // TODO 更新活动列表
      alert('刷新活动列表');
    },
  },
};
</script>

<style scoped>
/* TODO 调整按钮样式 */
.recommend-section {
  padding: 20px;
  background-color: white;
}

.recommend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.buttons button {
  padding: 10px 20px;
  margin-right: 10px;
  border: none;
  background-color: #f5f5f5;
  cursor: pointer;
}

.buttons button.active {
  background-color: #ff5733;
  color: white;
}

.refresh-button {
  padding: 10px 20px;
  background-color: #ff5733;
  color: white;
  border: none;
  cursor: pointer;
}

.activity-cards {
  display: flex;
  justify-content: space-between;
}
</style>
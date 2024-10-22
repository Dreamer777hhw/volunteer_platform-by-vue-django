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
          <button :class="{'active': currentTab === 'recommend'}" @click="currentTab = 'recommend'">猜你喜欢</button>
          <button :class="{'active': currentTab === 'hot'}" @click="currentTab = 'hot'">热门活动</button>
        </div>
        <button class="refresh-button" @click="refreshItems">刷新</button>
      </div>

      <!-- 活动卡片列表 -->
      <ActivityCardRow :activities="filteredActivities" />
    </div>
  </div>
</template>

<script>
import ActivityCardRow from '@/components/ActivityCardRow.vue';

export default {
  name: 'RecommendComponent',
  components: {
    ActivityCardRow,
  },
  data() {
    return {
      currentTab: 'recommend', // 默认显示“猜你喜欢”标签页
      activities: [
        // 假设的静态活动数据
        // TODO 从后端获取真实数据
        {
          image: 'activity-images/activity-11.jpg',
          title: '旋律欣赏活动1',
          host: '艺术学院',
          label: '劳动教育',
          participants: '60 / 60 人',
          registrationPeriod: '2024-10-12 ~ 2024-10-23',
          location: '图书馆',
          activityPeriod: '2024-10-10 ~ 2024-10-21',
        },
        {
          image: 'activity-images/activity-11.jpg',
          title: '旋律欣赏活动2',
          host: '艺术学院',
          label: '文体活动',
          participants: '60 / 60 人',
          registrationPeriod: '2024-10-12 ~ 2024-10-23',
          location: '图书馆',
          activityPeriod: '2024-10-10 ~ 2024-10-21',
        },
        {
          image: 'activity-images/activity-21.jpg',
          title: '志愿招募活动',
          host: '志愿者组织',
          label: '志愿公益',
          participants: '20 / 20 人',
          registrationPeriod: '2024-10-10 ~ 2024-10-14',
          location: '创新中心',
          activityPeriod: '2024-10-11 ~ 2024-10-15',
        },
        {
          image: 'activity-images/activity-21.jpg',
          title: '科技创新活动',
          host: '科技学院',
          label: '科创活动',
          participants: '30 / 30 人',
          registrationPeriod: '2024-10-15 ~ 2024-10-20',
          location: '科技园',
          activityPeriod: '2024-10-21 ~ 2024-10-25',
        },
      ],
    };
  },
  computed: {
    /**
     * @description 根据当前标签页过滤活动
     * @return {Array} 过滤后的活动
     */
    filteredActivities() {
      if (this.currentTab === 'recommend') {
        return this.activities.slice(0, 3); // 只显示前三个活动
      } else if (this.currentTab === 'hot') {
        return this.activities.slice(1, 4); // 假设热门活动是接下来的三个活动
      }
      return [];
    },
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
.recommend-container {
  justify-content: center;
}

.recommend-section {
  width: 1200px; 
  height: 600px; 
  background-color: white;
  display: relative;
  flex-direction: column;
  align-items: center;
}

.recommend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
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
</style>
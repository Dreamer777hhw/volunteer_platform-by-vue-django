<!--
    * @FileDescription: 推荐活动组件，包含猜你喜欢和热门活动两个标签页，以及活动卡片列表
    * @Author: infinity
    * @Date: 2024-10-31
    * @LastEditors: dreamer777hhw
    * @LastEditTime: 2024-11-04
 -->

<template>
  <div class="recommend-container">
    <div class="recommend-section">
      <div class="recommend-header">
        <div class="buttons">
          <button :class="{'active': currentTab === 'recommend'}" @click="fetchActivities('recommend')">
            <i class="icon-recommend"></i>猜你喜欢
          </button>
          <button :class="{'active': currentTab === 'hot'}" @click="fetchActivities('hot')">
            <i class="icon-hot"></i>热门活动
          </button>
          <button :class="{'active': currentTab === 'calendar'}" @click="currentTab = 'calendar'">
            <i class="icon-calendar"></i>活动日历
          </button>
          <button :class="{'active': currentTab === 'upcoming'}" @click="fetchUpcomingActivities">
            <i class="icon-calendar"></i>即将到来
          </button>
        </div>
      </div>

      <!-- 根据当前标签页显示不同的内容 -->
      <div v-if="currentTab === 'calendar'" class="calendar-tab">
        <CalendarComponent />
      </div>
      <div v-if="currentTab === 'recommend' || currentTab === 'hot'"  >
        <ActivityCardRow :activities="filteredActivities" />
      </div>
      <div v-if="currentTab === 'upcoming'">
        <ActivityCardRow :activities="upcomingActivitiescard" />
      </div>
    </div>
  </div>
</template>

<script>
import ActivityCardRow from '@/components/ActivityCardRow.vue';
import CalendarComponent from '@/components/CalendarComponent.vue';
// import UpcomingActivity from '@/components/UpcomingActivity.vue';
import axios from 'axios';

export default {
  name: 'RecommendComponent',
  components: {
    ActivityCardRow,
    CalendarComponent,
    // UpcomingActivity,
  },
  data() {
    return {
      currentTab: 'recommend', // 默认显示“猜你喜欢”标签页
      activities: [],
      upcomingActivities: [],
    };
  },
  computed: {
    /**
     * @description 过滤后的活动数据
     * @return {Array} 返回获取到的活动数据
     */
    upcomingActivitiescard() {
      return this.upcomingActivities;
    },
    filteredActivities() {
      return this.activities;
    },
  },
  methods: {
    /**
     * @description 获取活动数据
     * @param {string} tab 当前标签页（'recommend' 或 'hot'）
     * @return {void}
     */
    async fetchActivities(tab) {
      if (tab === 'calendar') return; // 如果是“活动日历”标签页，不请求活动数据

      try {
        this.currentTab = tab; // 更新当前标签
        const username = localStorage.getItem('username');
        const response = await axios.get(`http://127.0.0.1:8000/api/recommend/${tab}/${username}`);
        this.activities = response.data;
      } catch (error) {
        console.error('获取活动失败:', error);
      }
    },
    async fetchUpcomingActivities() {
      this.currentTab = 'upcoming'; // 更新当前标签
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/upcoming-activities/');
        this.upcomingActivities = response.data;
      } catch (error) {
        console.error('获取即将到来的活动失败:', error);
      }
    },
  },
  mounted() {
    this.fetchActivities(this.currentTab); // 初始化时加载活动
  },
};
</script>

<style scoped>
.buttons {
  display: flex;
  gap: 20px;
}

button {
  font-size: 24px;
  border: none;
  background: none;
  display: flex;
  align-items: center;
  cursor: pointer;
  padding-bottom: 10px;
}

button i {
  margin-right: 8px;
}

button.active {
  color: orange;
}

</style>

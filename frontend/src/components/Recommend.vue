<!-- 
    * @FileDescription: 推荐活动组件，包含猜你喜欢和热门活动两个标签页，以及活动卡片列表
    * @Author: infinity 
    * @Date: 2024-10-31 
    * @LastEditors: dreamer777hhw
    * @LastEditTime: 2024-11-02
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
        </div>
      </div>

      <!-- 根据当前标签页显示不同的内容 -->
      <div v-if="currentTab === 'calendar'" class="calendar-tab">
        <CalendarComponent />
      </div>
      <div v-else>
        <!-- 活动卡片列表，适用于“猜你喜欢”和“热门活动” -->
        <ActivityCardRow :activities="filteredActivities" />
      </div>
    </div>
  </div>
</template>

<script>
import ActivityCardRow from '@/components/ActivityCardRow.vue';
import CalendarComponent from '@/components/CalendarComponent.vue';
import axios from 'axios';

export default {
  name: 'RecommendComponent',
  components: {
    ActivityCardRow,
    CalendarComponent,
  },
  data() {
    return {
      currentTab: 'recommend', // 默认显示“猜你喜欢”标签页
      activities: [],
    };
  },
  computed: {
    /**
     * @description 过滤后的活动数据
     * @return {Array} 返回获取到的活动数据
     */
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

.calendar-tab {
  padding: 20px;
}
</style>

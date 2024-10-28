<!--
    * @FileDescription: 活动列表组件，包含活动筛选、排序和展示功能
    * @Author: infinity
    * @Date: 2024-10-22
    * @LastEditors: dreamer777hhw
    * @LastEditTime: 2024-10-28
 -->

<template>
  <div>
    <h1>所有活动</h1>

    <div class="filter-row">
      <button @click="clearFilters">全部</button>
      <label v-for="label in labels" :key="label">
        <input type="checkbox" v-model="selectedLabels" :value="label"> {{ label }}
      </label>
    </div>

    <div class="filter-row">
      <label v-for="status in statuses" :key="status">
        <input type="checkbox" v-model="selectedStatuses" :value="status"> {{ status }}
      </label>
    </div>

    <div class="filter-row">
      <input type="text" v-model="searchQuery" placeholder="搜索活动名称" />
      <select v-model="sortBy">
        <option value="time">按时间排序</option>
        <option value="participants">按可报名人数排序</option>
      </select>
    </div>

    <div>
      <ActivityCardRow
        v-for="(activityRow, index) in activityRows"
        :key="index"
        :activities="activityRow"
      />
    </div>

    <div ref="loadMoreTrigger" class="load-more-trigger"></div>
  </div>
</template>

<script>
import ActivityCardRow from '@/components/ActivityCardRow.vue';
import axios from 'axios';

export default {
  name: "ActivityListComponent",
  components: {
    ActivityCardRow,
  },
  data() {
    return {
      labels: ["讲坛讲座", "志愿公益", "劳动教育", "文体活动", "实习实践", "学习培训", "科创活动"],
      statuses: ["未开始", "招募中", "进行中"],
      selectedLabels: [],
      selectedStatuses: [],
      searchQuery: "",
      sortBy: "time",
      activities: [],
      currentPage: 1,
      itemsPerPage: 15,
    };
  },
  computed: {
    filteredActivities() {
      return this.activities
        .filter(activity => {
          if (this.selectedLabels.length > 0 && !this.selectedLabels.includes(activity.activity_tags)) {
            return false;
          }
          if (this.selectedStatuses.length > 0 && !this.selectedStatuses.includes(activity.status)) {
            return false;
          }
          if (this.searchQuery && !activity.activity_name.includes(this.searchQuery)) {
            return false;
          }
          return true;
        })
        .sort((a, b) => {
          if (this.sortBy === "time") {
            return new Date(a.activity_start_time) - new Date(b.activity_start_time);
          } else if (this.sortBy === "participants") {
            return b.accepted_volunteers - a.accepted_volunteers;
          }
        });
    },
    activityRows() {
      const rows = [];
      const totalActivities = this.filteredActivities.length;

      for (let i = 0; i < Math.min(totalActivities, this.currentPage * this.itemsPerPage); i += 3) {
        rows.push(this.filteredActivities.slice(i, i + 3));
      }

      return rows;
    },
  },
  methods: {
    clearFilters() {
      this.selectedLabels = [];
      this.selectedStatuses = [];
      this.searchQuery = "";
      this.currentPage = 1; // Reset page on filter clear
      this.fetchActivities(); // Re-fetch activities
    },
    async fetchActivities() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/activities/');
        this.activities = response.data;
      } catch (error) {
        console.error('获取活动数据失败:', error);
      }
    },
    setupIntersectionObserver() {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.loadMore();
          }
        });
      });

      observer.observe(this.$refs.loadMoreTrigger);
    },
    loadMore() {
      if (this.filteredActivities.length > this.currentPage * this.itemsPerPage) {
        this.currentPage++;
      }
    },
  },
  mounted() {
    this.fetchActivities();
    this.setupIntersectionObserver(); // 设置 IntersectionObserver
  }
};
</script>

<style scoped>
.filter-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.load-more-trigger {
  height: 1px; /* 不占空间 */
}
</style>

<!--
    * @FileDescription: 活动列表组件，包含活动筛选、排序和展示功能
    * @Author: infinity
    * @Date: 2024-10-22
    * @LastEditors: infinity
    * @LastEditTime: 2024-11-04
 -->

<template>
  <div>
    <h1 class="title">所有活动</h1>

    <div class="filter-container">
      <div class="filter-row">
        <button class="clear-button" @click="clearFilters">全部</button>
        <label v-for="label in labels" :key="label" class="filter-label">
          <input type="checkbox" v-model="selectedLabels" :value="label" class="filter-checkbox"> {{ label }}
        </label>
      </div>

      <hr class="divider">

      <div class="filter-row">
        <label v-for="status in statuses" :key="status" class="filter-label">
          <input type="checkbox" v-model="selectedStatuses" :value="status" class="filter-checkbox"> {{ status }}
        </label>
      </div>

      <hr class="divider">

      <div class="filter-row">
        <input type="text" v-model="searchQuery" placeholder="搜索活动名称" class="search-input" />
        <select v-model="sortBy" class="sort-select">
          <option value="time">按时间排序</option>
          <option value="participants">按可报名人数排序</option>
        </select>
      </div>
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
      statuses: ["未开始", "招募中", "已招满", '进行中', '已结束', '已取消'],
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
          if (this.selectedStatuses.length > 0 && !this.selectedStatuses.includes(activity.activity_status)) {
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
        const response = await axios.get('http://127.0.0.1:8000/api/activitieslist/');
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
.title {
  color: #666;
  font-size: 1.4em;
}

.filter-container {
  background-color: #fff;
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  margin-bottom: 15px;
}

.clear-button {
  font-size: 1em;
  border: none;
  background: transparent;
  cursor: pointer;
}

.filter-label {
  display: flex;
  align-items: center;
  font-size: 1em;
  color: #666;
}

.filter-checkbox {
  width: 1em;
  height: 1em;
  margin-right: 5px;
}

.divider {
  width: 100%;
  border: 0;
  border-top: 1px solid #ccc;
  /* 略微透明 */
  opacity: 0.3;
  margin: 10px 0;
}

.search-input {
  /* flex: 1; */
  padding: 7px;
  border-radius: 5px;
  border: 1px solid #ccc;
  width: 25%;
}

.sort-select {
  padding: 7px;
  border-radius: 5px;
  border: 1px solid #ccc;
  /* 右对齐 */
  margin-left: auto;

}

.load-more-trigger {
  height: 1px; /* 不占空间 */
}
</style>
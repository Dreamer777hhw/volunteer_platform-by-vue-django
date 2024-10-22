<!-- 
    * @FileDescription: 活动列表组件，包含活动筛选、排序和展示功能
    * @Author: infinity 
    * @Date: 2024-10-22 
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-22 
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

    <ActivityCardRow :activities="filteredActivities.slice(0,3)" />
    <!-- TODO 显示更多行卡片 -->

  </div>
</template>

<script>
import ActivityCardRow from '@/components/ActivityCardRow.vue';

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
      Activities: [
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
      visibleActivities: [],
      itemsPerPage: 15,
      currentPage: 1,
    };
  },
  computed: {
    /**
     * @description 根据筛选条件和排序规则过滤活动
     * @return {Array} 过滤后的活动列表
     */
    filteredActivities() {
      return this.Activities
        .filter((activity) => {
          // 标签筛选
          if (this.selectedLabels.length > 0 && !this.selectedLabels.includes(activity.label)) {
            return false;
          }
          // 状态筛选
          if (this.selectedStatuses.length > 0 && !this.selectedStatuses.includes(activity.status)) {
            return false;
          }
          // 搜索过滤
          if (this.searchQuery && !activity.title.includes(this.searchQuery)) {
            return false;
          }
          return true;
        })
        .sort((a, b) => {
          // TODO 实现排序功能
          if (this.sortBy === "time") {
            return new Date(a.activityPeriod) - new Date(b.activityPeriod);
          } else if (this.sortBy === "participants") {
            return b.participants - a.participants;
          }
        });
    },
  },
  methods: {
    /**
     * @description 清除所有筛选条件
     * @return {void}
     */
    clearFilters() {
      this.selectedLabels = [];
      this.selectedStatuses = [];
    },
    /**
     * @description 加载更多活动
     * @return {void}
     */
    loadMore() {
      const nextPageActivities = this.filteredActivities.slice(this.currentPage * this.itemsPerPage, (this.currentPage + 1) * this.itemsPerPage);
      this.visibleActivities = this.visibleActivities.concat(nextPageActivities);
      this.currentPage++;
    },
    /**
     * @description 设置 IntersectionObserver 以检测用户是否滚动到底部
     * @return {void}
     */
    setupIntersectionObserver() {
      const options = {
        root: null,
        rootMargin: '0px',
        threshold: 1.0
      };

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.loadMore();
          }
        });
      }, options);

      observer.observe(this.$refs.loadMoreTrigger);
    }
  },
  mounted() {
    this.loadMore(); // 初始加载活动
    this.setupIntersectionObserver(); // 设置 IntersectionObserver
  }
};
</script>

<style scoped>
/* TODO 按钮和复选框样式 */
/* TODO 背景与边框 */
.filter-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

button {
  margin: 5px;
}
</style>
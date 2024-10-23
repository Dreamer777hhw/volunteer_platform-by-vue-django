<!-- 
    * @FileDescription: Information 视图组件，展示用户的活动信息 
    * @Author: infinity
    * @Date: 2024-10-23 
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-23
 -->

<template>
  <div>
    <NavBar />
    <div class="activities-container">
      <div class="sidebar">
        <h3>我的</h3>
        <ul>
          <li>我的活动</li>
        </ul>
      </div>
      <div class="content">
        <div class="filter-bar">
          <div class="filter-dropdown">
            <select v-model="selectedStatus" @change="filterByStatus">
              <option value="" disabled selected>选择状态</option>
              <option value="未参与">未参与</option>
              <option value="参与中">参与中</option>
              <option value="已参与">已参与</option>
            </select>
          </div>
          <div class="search-bar">
            <input
              type="text"
              placeholder="按回车搜索名称、地点、主办方"
              v-model="searchQuery"
              @keyup.enter="searchActivities"
            />
          </div>
        </div>

        <div class="activity-table-header">
          <span>活动名称</span>
          <span>主办方</span>
          <span>状态</span>
        </div>

        <div class="activity-list">
          <div v-for="activity in paginatedActivities" :key="activity.title" class="activity-row">
            <ActivityCard :activity="activity" />
            <span>{{ activity.host }}</span>
            <span>{{ activity.status }}</span>
          </div>
        </div>
<!-- TODO 分页操作 -->
        <el-pagination
          layout="prev, pager, next"
          :page-size="activitiesPerPage"
          :total="filteredActivities.length"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import ActivityCard from '@/components/ActivityCard.vue'
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'InformationView',
  components: {
    ActivityCard,
    NavBar,
  },
  data() {
    return {
      searchQuery: '',
      selectedStatus: '',
      activities: [
        {
          image: 'activity-images/activity-11.jpg',
          title: '旋律欣赏活动1',
          host: '艺术学院',
          label: '劳动教育',
          participants: '60 / 60 人',
          registrationPeriod: '2024-10-12 ~ 2024-10-23',
          location: '图书馆',
          activityPeriod: '2024-10-10 ~ 2024-10-21',
          status: '未参与',
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
          status: '未参与',
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
          status: '参与中',
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
          status: '已参与',
        },
      ],
      filteredActivities: [],
      currentPage: 1,
      activitiesPerPage: 5,
    }
  },
  methods: {
    /** 
     * @description 根据状态筛选活动 
     * @param {Event} event - 事件对象 
     * @return {void}
     */
    filterByStatus(event) {
      this.selectedStatus = event.target.value
      this.applyFilters()
    },
    /** 
     * @description 搜索活动 
     * @return {void}
     */
    searchActivities() {
      this.applyFilters()
    },
    /** 
     * @description 应用筛选条件 
     * @return {void}
     */
    applyFilters() {
      this.filteredActivities = this.activities.filter(activity => {
        const matchesSearch =
          activity.title.includes(this.searchQuery) ||
          activity.host.includes(this.searchQuery) ||
          activity.location.includes(this.searchQuery)

        const matchesStatus =
          !this.selectedStatus || activity.status === this.selectedStatus

        return matchesSearch && matchesStatus
      })
    },
    /** 
     * @description 处理分页变化 
     * @param {number} page - 当前页码 
     * @return {void}
     */
    handlePageChange(page) {
      this.currentPage = page
    },
  },
  computed: {
    /** 
     * @description 获取当前页的活动 
     * @return {Array} 当前页的活动列表 
     */
    paginatedActivities() {
      const start = (this.currentPage - 1) * this.activitiesPerPage
      const end = start + this.activitiesPerPage
      return this.filteredActivities.slice(start, end)
    },
  },
  mounted() {
    this.filteredActivities = this.activities
  },
}
</script>

<style scoped>
/* TODO 样式调整 */
.activities-container {
  display: flex;
  width: 80%;
  margin: 100px auto;
  border: 1px solid #ddd;
}
.sidebar {
  width: 120px;
  padding: 20px;
  border: 1px solid #ddd;
}
.content {
  flex-grow: 1;
  padding: 20px;
  border: 1px solid #ddd;
}
.filter-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  border: 1px solid #ddd;
}
.activity-table-header {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
}
.activity-table-header span {
  flex-basis: 40%;
  text-align: center;
}
.activity-table-header span:nth-child(2) {
  flex-basis: 32%;
}
.activity-table-header span:nth-child(3) {
  flex-basis: 28%;
}
.activity-list {
  margin-top: 10px;
  border: 1px solid #ddd;
}

.activity-list span {
  flex-basis: 40%;
  text-align: center;
}
.activity-list span:nth-child(2) {
    flex-basis: 30%;
}
.activity-list span:nth-child(3) {
    flex-basis: 30%;
} 
.activity-row {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}
</style>
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
              <option value="已报名">已报名</option>
              <option value="已录取">已录取</option>
              <option value="未录取">未录取</option>
              <option value="已取消">已取消</option>
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
          <div v-for="activity in activities" :key="activity.id" class="activity-row">
            <ActivityCard :activity="activity" />
            <span>{{ activity.host }}</span>
            <span>{{ activity.activity_result }}</span>
          </div>
        </div>

        <el-pagination
          layout="prev, pager, next"
          :page-size="activitiesPerPage"
          :total="totalActivities"
          @current-change="handlePageChange"
          :current-page="currentPage"
        />
      </div>
    </div>
  </div>
</template>

<script>
import ActivityCard from '@/components/ActivityCard.vue'
import NavBar from '@/components/NavBar.vue'
import axios from 'axios'

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
      activities: [],
      totalActivities: 0,
      currentPage: 1,
      activitiesPerPage: 4,
    }
  },
  methods: {
    async fetchActivities() {
      const response = await axios.get(`http://127.0.0.1:8000/api/user-activities/`, {
        params: {
          page: this.currentPage,
          status: this.selectedStatus,
          search: this.searchQuery,
          user_id: localStorage.getItem('username'), // 获取 user_id
        },
      });
      this.activities = response.data.results; // 更新活动列表
      this.totalActivities = response.data.count; // 更新总活动数
    },
    filterByStatus() {
      this.currentPage = 1; // 重置到第一页
      this.fetchActivities();
    },
    searchActivities() {
      this.currentPage = 1; // 重置到第一页
      this.fetchActivities();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchActivities();
    },
  },
  mounted() {
    this.fetchActivities(); // 初始化时加载活动
  },
}
</script>

<style scoped>
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
.activity-row {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}
</style>

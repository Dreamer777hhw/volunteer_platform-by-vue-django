<!-- 
    * @FileDescription: Information 视图组件，展示用户的活动信息 
    * @Author: infinity
    * @Date: 2024-10-23 
    * @LastEditors: dreamer777hhw
    * @LastEditTime: 2024-11-04
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
              <option value="all">全选</option>
              <option v-for="status in availableStatuses" :key="status" :value="status">{{ status }}</option>
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

        <button class="create-activity-btn" @click="navigateToCreateActivity">创建活动</button>

        <div class="activity-table-header">
          <span>活动名称</span>
          <span>主办方</span>
          <span>状态</span>
        </div>

        <div class="activity-list">
          <div v-for="activity in activities" :key="activity.id" class="activity-row">
            <ActivityCard :activity="activity" />
            <span>{{ activity.organizer_name }}</span>
            <span>{{ getActivityResult(activity) }}</span>
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
  computed: {
    availableStatuses() {
      return this.isOrganizer
        ? ['未开始', '招募中', '已招满', '进行中', '已结束', '已取消']
        : ['未参与', '参与中', '已参与', '已报名', '已录取', '未录取', '已取消'];
    },
    isOrganizer() {
      return localStorage.getItem('user_type') === 'organizer';
    },
  },
  methods: {
    async fetchActivities() {
      const response = await axios.get(`http://127.0.0.1:8000/api/user-activities/`, {
        params: {
          page: this.currentPage,
          status: this.selectedStatus,
          search: this.searchQuery,
          user_id: localStorage.getItem('username'), // 获取 user_id
          user_type: localStorage.getItem('user_type'), // 获取 user_type
        },
      });
      this.activities = response.data.results; // 更新活动列表
      this.totalActivities = response.data.count; // 更新总活动数
    },
    filterByStatus() {
      if (this.selectedStatus === 'all') {
        this.selectedStatus = ''; // 清空选择条件
      }
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
    navigateToCreateActivity() {
      this.$router.push('/activity/create');
    },
    getActivityResult(activity) {
      return this.isOrganizer
        ? activity.organizer_activity_result // 组织者活动状态
        : activity.volunteer_activity_result; // 志愿者活动状态
    },
  },
  mounted() {
    this.fetchActivities(); // 初始化时加载活动
  },
}
</script>

<style scoped>
/* 这里保持原样，不需要修改 */
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
.activity-row span {
  flex-basis: 40%;
  text-align: center;
}

button {
  margin-top: 10px;
  padding: 5px 10px;
  border: none;
  background-color: #4CAF50;
  color: white;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
.activities-container {
  display: flex;
  width: 80%;
  margin: 100px auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.sidebar {
  width: 150px;
  padding: 20px;
  border-right: 1px solid #ddd;
}

.content {
  flex-grow: 1;
  padding: 20px;
}

.create-activity-btn {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px; /* 添加底部间距 */
  transition: background-color 0.3s;
}

.create-activity-btn:hover {
  background-color: #45a049;
}

.filter-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.activity-table-header {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.activity-list {
  margin-top: 10px;
}

.activity-row {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  transition: background-color 0.2s;
}

.activity-row:hover {
  background-color: #f1f1f1;
}

.activity-row span {
  flex-basis: 30%;
  text-align: center;
}

.search-bar input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 250px;
}

.filter-dropdown select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>


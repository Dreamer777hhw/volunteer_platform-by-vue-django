<!-- 
    * @FileDescription: Information 视图组件，展示用户的活动信息 
    * @Author: infinity
    * @Date: 2024-10-23 
    * @LastEditors: infinity
    * @LastEditTime: 2024-11-04
 -->

<template>
  <div class="information">
    <NavBar />
    <div class="activities-container">
      <div class="sidebar">
        <h3>我的</h3>
        <ul>
          <li @click="navigateToCurrentPage" class="sidebar-item">我的活动</li>
          <li v-if="isOrganizer" @click="navigateToCreateActivity" class="sidebar-item create-activity">创建活动</li>
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

        <div class="activity-table-header">
          <span>活动名称</span>
          <span>主办方</span>
          <span>状态</span>
        </div>

        <div class="activity-list">
          <div v-for="activity in activities" :key="activity.activity_id" class="activity-row">
            <ActivityCard :activity="activity" />
            <span>{{ activity.organizer_name }}</span>
            <span>{{ getActivityResult(activity) }}</span> <!-- 显示活动状态 -->
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
    /**
     * @description 获取可用的状态选项
     * @return {Array} 返回状态选项数组
     */
    availableStatuses() {
      return this.isOrganizer
        ? ['未开始', '招募中', '已招满', '进行中', '已结束', '已取消']
        : ['未参与', '参与中', '已参与', '已报名', '已录取', '未录取', '已取消'];
    },
    /**
     * @description 判断当前用户是否为组织者
     * @return {boolean} 返回当前用户是否为组织者
     */
    isOrganizer() {
      return localStorage.getItem('user_type') === 'organizer';
    },
  },
  methods: {
    /**
     * @description 获取用户活动数据
     * @return {void}
     */
    async fetchActivities() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/user-activities/`, {
          params: {
            page: this.currentPage,
            page_size: this.activitiesPerPage,  // 显示的每页活动数
            status: this.selectedStatus,
            search: this.searchQuery,
            user_id: localStorage.getItem('username'), // 获取 user_id
            user_type: localStorage.getItem('user_type'), // 获取 user_type
          },
        });
        this.activities = response.data.results; // 更新活动列表
        this.totalActivities = response.data.count; // 更新总活动数
      } catch (error) {
        console.error('Error fetching activities:', error);
      }
    },
    /**
     * @description 根据状态过滤活动
     * @return {void}
     */
    filterByStatus() {
      if (this.selectedStatus === 'all') {
        this.selectedStatus = ''; // 清空选择条件
      }
      this.currentPage = 1; // 重置到第一页
      this.fetchActivities();
    },
    /**
     * @description 根据搜索查询过滤活动
     * @return {void}
     */
    searchActivities() {
      this.currentPage = 1; // 重置到第一页
      this.fetchActivities();
    },
    /**
     * @description 处理分页变化
     * @param {number} page 当前页码
     * @return {void}
     */
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchActivities();
    },
    /**
     * @description 跳转到创建活动页面
     * @return {void}
     */
    navigateToCreateActivity() {
      this.$router.push('/activity/create');
    },
    /**
     * @description 跳转到当前页面
     * @return {void}
     */
    navigateToCurrentPage() {
      this.$router.push('/information');
    },
    /**
     * @description 获取活动状态
     * @param {Object} activity 活动对象
     * @return {string} 返回活动状态
     */
    getActivityResult(activity) {
      return activity.activity_result;
      // return this.isOrganizer
      //   ? activity.organizer_activity_result || '未知状态' // 组织者活动状态
      //   : activity.volunteer_activity_result || '未知状态'; // 志愿者活动状态
    }
  },
  mounted() {
    this.fetchActivities(); // 初始化时加载活动
  },
}
</script>

<style scoped>
.information {
  background-image: url('../../public/background/bg.webp');
  background-repeat: repeat;
  background-size: auto;
  background-position: center;
}

.activities-container {
  display: flex;
  width: 80%;
  margin: 100px auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
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

.filter-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.activity-table-header {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
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

.sidebar ul {
  list-style-type: none;
  padding: 0;
}

.sidebar-item {
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.sidebar-item:hover {
  background-color: #f0f0f0;
}

.create-activity {
  margin-top: 20px;
}
</style>
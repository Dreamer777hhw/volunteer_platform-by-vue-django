<!--
    * @FileDescription: 检查志愿者申请页面，用户可以在此页面查看和管理志愿者申请
    * @Author: infinity
    * @Date: 2024-10-24
    * @LastEditors: dreamer777hhw
    * @LastEditTime: 2024-11-04
 -->

<template>
  <div>
    <NavBar />
    <div class="check-volunteer-container">
      <div class="check-volunteer-card">
        <h2 class="check-volunteer-title">检查志愿者申请</h2>

        <div class="activity-details">
          <div class="activity-name">
            <label>活动名称：</label>
            <span>{{ activityName }}</span>
          </div>
          <div class="acceptance-status">
            <label>已录取人数：</label>
            <span>{{ acceptedVolunteers }} / {{ totalVolunteers }}</span>
          </div>
        </div>

        <div class="volunteer-list-header">
          <span>姓名</span>
          <span>学号</span>
          <span>专业</span>
          <span>学院</span>
          <span>邮箱</span>
          <span>手机号</span>
          <span>状态</span>
        </div>

        <div v-for="(item, index) in applicationVolunteerData" :key="index" class="volunteer-row">
            <span>{{ item.volunteer.name }}</span>
            <span>{{ item.volunteer.student_id }}</span>
            <span>{{ item.volunteer.major }}</span>
            <span>{{ item.volunteer.school }}</span>
            <span>{{ item.volunteer.email }}</span>
            <span>{{ item.volunteer.phone }}</span>
            <span>
              <template v-if="item.application.application_result === '已通过'">
                已通过
              </template>
              <template v-else-if="item.application.application_result === '未通过'">
                未通过
              </template>
              <template v-else>
                <div class="action-buttons">
                  <button @click="approveVolunteer(item.application.application_id)">同意</button>
                  <button @click="rejectVolunteer(item.application.application_id)">拒绝</button>
                </div>
              </template>
            </span>
        </div>


        <div class="pagination">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
          >
            上一页
          </button>

          <span>第 {{ currentPage }} 页</span>

          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
          >
            下一页
          </button>
        </div>

        <div class="bulk-action-buttons">
          <button @click="approveAll" class="bulk-button">一键同意</button>
          <button @click="rejectAll" class="bulk-button">一键拒绝</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';

export default {
  name: 'CheckVolunteerView',
  components: {
    NavBar,
  },
  data() {
    return {
      activity_id: this.$route.params.activity_id_hash,
      activityName: '',
      volunteers: [],
      applications: [],
      acceptedVolunteers: 0,
      totalVolunteers: 0,
      currentPage: 1, // 当前页码
      itemsPerPage: 10, // 每页显示的项数
      totalPages: 0, // 总页数
      applicationVolunteerData: [],
    };
  },
  computed: {
    // 获取当前页的数据
    paginatedApplications() {
      // const start = (this.currentPage - 1) * this.itemsPerPage;
      // const end = this.currentPage * this.itemsPerPage;
      return this.applications.slice(0, 9); // 获取当前页的数据
    },
  },
  mounted() {
    this.fetchVolunteerApplications();
  },
  methods: {
    // 请求获取志愿者申请数据
    fetchVolunteerApplications() {
      axios.get(`http://127.0.0.1:8000/api/applications/${this.activity_id}/?page=${this.currentPage}&page_size=${this.itemsPerPage}`)
        .then(response => {
          this.activityName = response.data.activity_name;
          this.applicationVolunteerData = response.data.applications_and_volunteers;
          this.acceptedVolunteers = response.data.registered_volunteers;
          this.totalVolunteers = response.data.accepted_volunteers;
          this.currentPage = response.data.current_page;
          this.totalPages = response.data.total_pages;
        })
        .catch(error => {
          console.error('获取申请记录失败:', error);
        });
    },
    // 页面跳转
    changePage(pageNumber) {
      if (pageNumber > 0 && pageNumber <= this.totalPages) {
        this.currentPage = pageNumber;
        this.fetchVolunteerApplications(); // 重新获取分页数据
      }
    },
    // 同意志愿者申请
    approveVolunteer(applicationId) {
      axios.patch(`http://127.0.0.1:8000/api/applications/approve/${applicationId}/`, { application_result: '已通过' })
        .then(response => {
          this.fetchVolunteerApplications();
          console.log('申请已同意:', response.data.message);
        })
        .catch(error => {
          console.error('同意申请失败:', error);
        });
    },
    // 拒绝志愿者申请
    rejectVolunteer(applicationId) {
      axios.patch(`http://127.0.0.1:8000/api/applications/reject/${applicationId}/`, { application_result: '未通过' })
        .then(response => {
          this.fetchVolunteerApplications();
          console.log('申请已拒绝:', response.data.message);
        })
        .catch(error => {
          console.error('拒绝申请失败:', error);
        });
    },
    // 一键同意所有申请
    approveAll() {
      axios.patch(`http://127.0.0.1:8000/api/applications/approve_all/${this.activity_id}/`)
        .then(response => {
          this.fetchVolunteerApplications();
          console.log('所有申请已同意', response.data.message);
        })
        .catch(error => {
          console.error('一键同意失败:', error);
        });
    },
    // 一键拒绝所有申请
    rejectAll() {
      axios.patch(`http://127.0.0.1:8000/api/applications/reject_all/${this.activity_id}/`)
        .then(response => {
          this.fetchVolunteerApplications();
          console.log('所有申请已拒绝', response.data.message);
        })
        .catch(error => {
          console.error('一键拒绝失败:', error);
        });
    },
  },
};
</script>

<style scoped>
.check-volunteer-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-image: url('../../public/background/bg.webp');
  background-repeat: repeat;
  background-size: auto;
  background-position: center;
}

.check-volunteer-card {
  margin-top: 80px;
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 1000px;
}

.check-volunteer-title {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.activity-details {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.activity-name,
.acceptance-status {
  font-size: 1rem;
  color: #333;
}

.volunteer-list-header,
.volunteer-row {
  display: grid;
  grid-template-columns: 100px 150px 100px 150px 200px 150px 150px;
  padding: 10px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
}

.volunteer-list-header {
  font-weight: bold;
}

.volunteer-row {
  background-color: white;
  border-top: none;
}

.volunteer-row span,
.volunteer-list-header span {
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.action-buttons {
  display: flex;
  justify-content: space-around;
}

.action-buttons button,
.bulk-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 0.3rem 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.action-buttons button:hover,
.bulk-button:hover {
  background-color: #0056b3;
}

.bulk-action-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

.bulk-button {
  font-size: 1rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 0.3rem 1rem;
  margin: 0 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pagination button:hover {
  background-color: #0056b3;
}

.pagination button:disabled {
  background-color: #d6d6d6;
  cursor: not-allowed;
}

.pagination span {
  font-size: 1rem;
}
</style>

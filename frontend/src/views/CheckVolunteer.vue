<!-- 
    * @FileDescription: 检查志愿者申请页面，用户可以在此页面查看和管理志愿者申请 
    * @Author: infinity
    * @Date: 2024-10-24 
    * @LastEditors: infinity
    * @LastEditTime: 2024-11-03
 -->

<template>
  <div>
    <NavBar />
    <div class="check-volunteer-container">
      <div class="check-volunteer-card">
        <h2 class="check-volunteer-title">检查志愿者申请</h2>
        <div class="activity-name">
          <label>活动名称：</label>
          <span>{{ activityName }}</span>
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
        <div class="volunteer-list">
          <div v-for="(application, index) in applications" :key="application.application_id" class="volunteer-row">
            <span>{{ volunteers[index].name }}</span>
            <span>{{ volunteers[index].student_id }}</span>
            <span>{{ volunteers[index].major }}</span>
            <span>{{ volunteers[index].school }}</span>
            <span>{{ volunteers[index].email }}</span>
            <span>{{ volunteers[index].phone }}</span>
            <span>
              <template v-if="application.application_result === '已通过'">
                已通过
              </template>
              <template v-else-if="application.application_result === '未通过'">
                未通过
              </template>
              <template v-else>
                <div class="action-buttons">
                  <button @click="approveVolunteer(application.application_id)">同意</button>
                  <button @click="rejectVolunteer(application.application_id)">拒绝</button>
                </div>
              </template>
            </span>
          </div>
        </div>
        <div class="bulk-action-buttons">
          <button @click="approveAll">一键同意</button>
          <button @click="rejectAll">一键拒绝</button>
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
    };
  },
  mounted() {
    this.fetchVolunteerApplications();
  },
  methods: {
    /**
     * @description 获取志愿者申请列表
     * @return {void}
     */
    fetchVolunteerApplications() {
      axios.get(`http://127.0.0.1:8000/api/applications/${this.activity_id}/`)
        .then(response => {
          this.activityName = response.data.activity_name; // 获取活动名称
          this.volunteers = response.data.volunteers; // 获取志愿者信息
          this.applications = response.data.applications; // 获取申请记录
        })
        .catch(error => {
          console.error('获取申请记录失败:', error);
        });
    },
    /**
     * @description 同意志愿者申请
     * @param {string} studentId 志愿者学号
     * @return {void}
     */
    approveVolunteer(studentId) {
      axios.patch(`http://127.0.0.1:8000/api/applications/approve/${studentId}/`, { application_result: '已通过' })
        .then(response => {
          this.fetchVolunteerApplications(); // 重新获取申请列表
          console.log('申请已同意:', response.data.message);
        })
        .catch(error => {
          console.error('同意申请失败:', error);
        });
    },
    /**
     * @description 拒绝志愿者申请
     * @param {string} studentId 志愿者学号
     * @return {void}
     */
    rejectVolunteer(studentId) {
      axios.patch(`http://127.0.0.1:8000/api/applications/reject/${studentId}/`, { application_result: '未通过' })
        .then(response => {
          this.fetchVolunteerApplications(); // 重新获取申请列表
          console.log('申请已拒绝:', response.data.message);
        })
        .catch(error => {
          console.error('拒绝申请失败:', error);
        });
    },
    /**
     * @description 一键同意所有志愿者申请
     * @return {void}
     */
    approveAll() {
      // 一键同意所有志愿者申请逻辑
      console.log('一键同意所有志愿者申请');
      // 需要实现一键同意的后端逻辑
    },
    /**
     * @description 一键拒绝所有志愿者申请
     * @return {void}
     */
    rejectAll() {
      // 一键拒绝所有志愿者申请逻辑
      console.log('一键拒绝所有志愿者申请');
      // 需要实现一键拒绝的后端逻辑
    }
  }
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

.activity-name {
  margin-bottom: 1rem;
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

.action-buttons button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 0.2rem 0.7rem;
  cursor: pointer;
}

.bulk-action-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.bulk-action-buttons button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>
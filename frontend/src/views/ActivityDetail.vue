<!-- 
    * @FileDescription: 活动详情页面，展示活动的详细信息 
    * @Author: infinity
    * @Date: 2024-10-24 
    * @LastEditors: dreamer777hhw
    * @LastEditTime: 2024-11-06
 -->

<template>
  <div>
    <NavBar />
    <div class="activity-detail-container">
      <div class="activity-detail-box">
        <div class="activity-view">
          <img :src="activity.activity_image_path" alt="活动图片" class="activity-image" />
          <div class="activity-info">
            <h1 class="activity-title">{{ activity.activity_name }}</h1>
            <p class="activity-time">{{ formatDateTime(activity.activity_start_time) }} - {{ formatDateTime(activity.activity_end_time) }}</p>
            <div class="activity-details">

              <p v-if="isBeforeRegistration" class="status-before-registration">报名未开始</p>

              <p v-if="isAfterRegistration" class="status-after-registration">报名已结束</p>

              <p v-if="activity.organizer">主办方: {{ activity.organizer }}</p>
              <p v-if="activity.contact_name">负责人姓名: {{ activity.contact_name }}</p>
              <p v-if="activity.contact_phone">负责人手机: {{ activity.contact_phone }}</p>
              <p v-if="activity.activity_tags">活动类型: {{ activity.activity_tags }}</p>
              <p v-if="activity.accepted_volunteers !== undefined">总录取人数: {{ activity.accepted_volunteers }}</p>
              <p v-if="activity.registered_volunteers !== undefined">已录取人数: {{ activity.registered_volunteers }}</p>
              <p v-if="activity.estimated_volunteer_hours">劳动时长: {{ activity.estimated_volunteer_hours }}</p>
              <p v-if="registrationPeriod">报名时间: {{ formatDateTime(activity.application_start_time) }} - {{ formatDateTime(activity.application_end_time) }}</p>
              <p v-if="activity.activity_location" class="activity-location">活动地点: {{ activity.activity_location }}</p>
              <p v-if="activity.sutuo">素拓: {{ activity.sutuo }}</p>
              <p v-if="activity.application_requirements">报名要求: {{ activity.application_requirements }}</p>

              <div v-if="isVolunteer">
                <p v-if="applicationStatus === '已通过'" class="status-approved">申请已通过</p>
                <p v-if="applicationStatus === '未通过'" class="status-denied">申请未通过</p>
                <button v-if="!isFull && applicationStatus === null && !hasRegistered && !isBeforeRegistration" class="register-button" @click="registerForActivity">
                  报名
                </button>
                <button v-if="!isFull && hasRegistered && applicationStatus === '待审核'" class="register-button" @click="cancelRegistration">
                  取消报名
                </button>
                <p v-if="isFull" class="status-isFull">报名人数已满</p>
              </div>

              <div v-if="isOrganizer && isRightOrganizer" class="organizer-buttons">
                <button class="register-button" @click="navigateToReviseActivity">修改活动</button>
                <button class="register-button" @click="navigateToCheckVolunteer">审核志愿者</button>
              </div>
            </div>
          </div>
        </div>
        <hr class="divider" />
        <div class="activity-description">
          <h2>活动描述</h2>
          <p>{{ activity.activity_description }}</p>
        </div>
        <div class="activity-notes">
          <h2>备注</h2>
          <p>{{ activity.notes }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  name: 'ActivityDetailView',
  components: {
    NavBar,
  },
  data() {
    return {
      activity: {},
      hasRegistered: false,
      applicationStatus: null, // 新增状态
      isRightOrganizer: false,
      isFull: false,
      isBeforeRegistration: false,
      isAfterRegistration: false,
    };
  },
  computed: {
    // isFull() {
    //   return this.activity.accepted_volunteers <= this.activity.registered_volunteers;
    // },
    registrationPeriod() {
      return `${this.activity.application_start_time} ~ ${this.activity.application_end_time}`;
    },
    isOrganizer() {
      return localStorage.getItem('user_type') === 'organizer';
    },
    isVolunteer() {
      return localStorage.getItem('user_type') === 'volunteer';
    },
  },
  methods: {
    async fetchActivityDetail() {
      const activityIdHash = this.$route.params.activity_id_hash;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/activity/${activityIdHash}/`);
        this.activity = response.data;
        // 检查是否是当前活动的组织者
        this.activity.organizer_id = String(this.activity.organizer_id);

        this.isBeforeRegistration = this.activity.activity_status === '未开始';
        this.isAfterRegistration = this.activity.activity_status === '已结束' || this.activity.activity_status === '进行中';

        this.isFull = this.activity.accepted_volunteers <= this.activity.registered_volunteers;

        this.isRightOrganizer = this.activity.organizer_id === localStorage.getItem('username');
        // 更新点击数
        await axios.post(`http://127.0.0.1:8000/api/activity/click/${this.activity.activity_id}/`);

        const userId = localStorage.getItem('username');
        const registrationsResponse = await axios.get(`http://127.0.0.1:8000/api/activity/${activityIdHash}/registrations/${userId}/`);
        if (registrationsResponse.data.some(data => data.activity_result === '已报名')) {
          this.hasRegistered = true;
        }

        // 获取申请状态
        const application = registrationsResponse.data.find(data => data.activity_result);
        if (application) {
          this.applicationStatus = application.application_result;
        }

      } catch (error) {
        console.error("获取活动详情失败:", error);
      }
    },
    /**
     * @description 报名参加活动
     * @return {void}
     */
    async registerForActivity() {
      const activityIdHash = this.$route.params.activity_id_hash;
      try {
        const response = await axios.post(`http://127.0.0.1:8000/api/activity/register/${activityIdHash}/${localStorage.getItem('username')}/`);
        // 用 ElMessage 显示成功信息
        ElMessage({
          message: response.data.message,
          type: 'success',
        });
        this.hasRegistered = true;
        this.fetchActivityDetail();
      } catch (error) {
        if (error.response) {
          // 用 ElMessage 显示错误信息
          ElMessage({
            message: error.response.data.error,
            type: 'error',
          });
        } else {
          ElMessage({
            message: '报名失败，请稍后再试！',
            type: 'error',
          });
          console.error("报名失败:", error);
        }
      }
    },
    /**
     * @description 取消报名
     * @return {void}
     */
    async cancelRegistration() {
      const activityIdHash = this.$route.params.activity_id_hash;
      try {
        const userId = localStorage.getItem('username');
        const response = await axios.post(`http://127.0.0.1:8000/api/activity/cancel/${activityIdHash}/${userId}/`);
        // 用 ElMessage 显示成功信息
        ElMessage({
          message: response.data.message,
          type: 'success',
        });
        this.hasRegistered = false; // 更新状态为未报名
        this.fetchActivityDetail(); // 重新获取活动详情以更新数据
        window.location.reload(); // 刷新页面
      } catch (error) {
        if (error.response) {
          // 用 ElMessage 显示错误信息
          ElMessage({
            message: error.response.data.error,
            type: 'error',
          });
        } else {
          ElMessage({
            message: '取消报名失败，请稍后再试！',
            type: 'error',
          });
          console.error("取消报名失败:", error);
        }
      }
    },

    /**
     * @description 跳转到修改活动页面
     * @return {void}
     */
    navigateToReviseActivity() {
      this.$router.push({ name: 'ReviseActivity', params: { activity_id_hash: this.activity.activity_id } });
    },
    /**
     * @description 跳转到审核志愿者页面
     * @return {void}
     */
    navigateToCheckVolunteer() {
      this.$router.push({ name: 'CheckVolunteer', params: { activity_id_hash: this.activity.activity_id } });
    },
    /**
     * @description 格式化日期时间
     * @param {string} dateTime 日期时间字符串
     * @return {string} 格式化后的日期时间字符串
     */
    formatDateTime(dateTime) {
      const date = new Date(dateTime);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${year}-${month}-${day} ${hours}:${minutes}`;
    },
  },
  mounted() {
    this.fetchActivityDetail();
  }
};
</script>

<style scoped>
.activity-detail-container {
  background-image: url('../../public/background/bg.webp');
  background-repeat: repeat;
  background-size: auto;
  background-position: center;
  margin-top: 80px;
  padding: 2rem;
  display: flex;
  justify-content: center;
}

.activity-detail-box {
  background-color: white;
  width: 80%;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.activity-view {
  display: flex;
  align-items: flex-start;
}

.activity-image {
  margin-top: 10px;
  width: 20%;
  /* height: 300px; */
  object-fit: cover;
}

.activity-info {
  flex: 1;
  padding-left: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.activity-title {
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
}

.activity-time {
  color: #888;
  margin-top: 0;
  font-size: 1rem;
}

.activity-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-size: 1rem;
}

.activity-details p {
  margin: 0.3rem;
}

.activity-location {
  margin-top: auto;
}

.register-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  margin-top: 1rem;
  width: 100px;
}

.register-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.divider {
  border: none;
  border-top: 1px solid #ccc;
  margin: 2rem 0;
}

.activity-description,
.activity-notes {
  margin-top: 2rem;
}

.activity-description h2,
.activity-notes h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.activity-description p,
.activity-notes p {
  font-size: 1rem;
  color: #333;
}

.organizer-buttons {
  display: flex;
  gap: 1rem; /* 按钮之间的间隔 */
  margin-top: 1rem; /* 上方间距 */
}

.register-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  width: 120px; /* 设置按钮宽度 */
  transition: background-color 0.3s; /* 添加过渡效果 */
}

.register-button:hover {
  background-color: #0056b3; /* 悬停时的背景色 */
}

.register-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.status-approved {
  color: green;
  font-weight: bold;
}

.status-denied {
  color: red;
  font-weight: bold;
}

.status-before-registration {
  color: orange;
  font-weight: bold;
}

.status-after-registration {
  color: red;
  font-weight: bold;
}

.status-isFull {
  color: red;
  font-weight: bold;
}

</style>
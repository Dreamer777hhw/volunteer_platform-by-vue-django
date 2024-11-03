<!-- 
    * @FileDescription: 活动详情页面，展示活动的详细信息 
    * @Author: infinity
    * @Date: 2024-10-24 
    * @LastEditors: infinity
    * @LastEditTime: 2024-11-03
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
              <p v-if="activity.organizer">主办方: {{ activity.organizer }}</p>
              <p v-if="activity.contact_name">负责人姓名: {{ activity.contact_name }}</p>
              <p v-if="activity.contact_phone">负责人手机: {{ activity.contact_phone }}</p>
              <p v-if="activity.activity_tags">活动类型: {{ activity.activity_tags }}</p>
              <p v-if="activity.accepted_volunteers !== undefined">
                总录取人数: {{ activity.accepted_volunteers }}
              </p>
              <p v-if="activity.registered_volunteers !== undefined">
                已录取人数: {{ activity.registered_volunteers }}
              </p>
              <p v-if="activity.estimated_volunteer_hours">劳动时长: {{ activity.estimated_volunteer_hours }}</p>
              <p v-if="registrationPeriod">报名时间: {{ formatDateTime(activity.application_start_time) }} - {{ formatDateTime(activity.application_end_time) }}</p>
              <p v-if="activity.activity_location" class="activity-location">
                活动地点: {{ activity.activity_location }}
              </p>
              <div v-if="isVolunteer">
                <button class="register-button" :disabled="isFull || hasRegistered" @click="registerForActivity">
                  {{ isFull ? '报名已满' : hasRegistered ? '已报名' : '报名' }}
                </button>
                <button v-if="hasRegistered" class="register-button" @click="cancelRegistration">
                  取消报名
                </button>
              </div>
              <div v-if="isOrganizer">
                <button class="register-button" @click="navigateToReviseActivity">修改活动</button>
              </div>
              <div v-if="isOrganizer">
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

export default {
  name: 'ActivityDetailView',
  components: {
    NavBar,
  },
  data() {
    return {
      activity: {},
      hasRegistered: false,
    };
  },
  computed: {
    /**
     * @description 判断活动是否已满员
     * @return {boolean} 返回活动是否已满员
     */
    isFull() {
      return this.activity.accepted_volunteers <= this.activity.registered_volunteers;
    },
    /**
     * @description 获取报名时间段
     * @return {string} 返回报名时间段
     */
    registrationPeriod() {
      return `${this.activity.application_start_time} ~ ${this.activity.application_end_time}`;
    },
    /**
     * @description 判断当前用户是否为组织者
     * @return {boolean} 返回当前用户是否为组织者
     */
    isOrganizer() {
      return localStorage.getItem('user_type') === 'organizer';
    },
    /**
     * @description 判断当前用户是否为志愿者
     * @return {boolean} 返回当前用户是否为志愿者
     */
    isVolunteer() {
      return localStorage.getItem('user_type') === 'volunteer';
    },
  },
  methods: {
    /**
     * @description 获取活动详情
     * @return {void}
     */
    async fetchActivityDetail() {
      const activityIdHash = this.$route.params.activity_id_hash;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/activity/${activityIdHash}/`);
        this.activity = response.data;

        const userId = localStorage.getItem('username');
        const registrationsResponse = await axios.get(`http://127.0.0.1:8000/api/activity/${activityIdHash}/registrations/${userId}/`);
        if (registrationsResponse.data.some(data => data.activity_result === '已报名')) {
          this.hasRegistered = true;
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
        alert(response.data.message);
        this.hasRegistered = true;
        this.fetchActivityDetail();
      } catch (error) {
        if (error.response) {
          alert(error.response.data.error);
        } else {
          alert('报名失败，请稍后再试！');
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
        alert(response.data.message);
        this.hasRegistered = false; // 更新状态为未报名
        this.fetchActivityDetail(); // 重新获取活动详情以更新数据
      } catch (error) {
        if (error.response) {
          alert(error.response.data.error);
        } else {
          alert('取消报名失败，请稍后再试！');
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
</style>
<!-- 
    * @FileDescription: 活动详情页面，展示活动的详细信息 
    * @Author: infinity
    * @Date: 2024-10-24 
    * @LastEditors: dreamer777hhw
    * @LastEditTime: 2024-10-31
 -->

<template>
  <div>
    <NavBar />
    <div class="activity-detail-container">
      <div class="activity-view">
        <img :src="activity.activity_image_path" alt="活动图片" class="activity-image" />
        <div class="activity-info">
          <h1 class="activity-title">{{ activity.activity_name }}</h1>
          <p class="activity-time">{{ activityPeriod }}</p>
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
            <p v-if="activity.clicks_in_1h !== undefined">
              1小时点击数: {{ activity.clicks_in_1h }}
            </p>
            <p v-if="activity.clicks_in_12h !== undefined">
              12小时点击数: {{ activity.clicks_in_12h }}
            </p>
            <p v-if="activity.total_clicks !== undefined">
              总点击数: {{ activity.total_clicks }}
            </p>
            <p v-if="activity.estimated_volunteer_hours">劳动时长: {{ activity.estimated_volunteer_hours }}</p>
            <p v-if="registrationPeriod">报名时间: {{ registrationPeriod }}</p>
            <p v-if="activity.activity_location" class="activity-location">
              活动地点: {{ activity.activity_location }}
            </p>
            <div v-if="isVolunteer">
              <button class="register-button" :disabled="isFull || hasRegistered" @click="registerForActivity">
                {{ isFull ? '报名已满' : hasRegistered ? '已报名' : '报名' }}
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
      hasRegistered: false, // 新增变量来判断用户是否已报名
    };
  },
  computed: {
    isFull() {
      return this.activity.accepted_volunteers <= this.activity.registered_volunteers;
    },
    activityPeriod() {
      return `${this.activity.activity_start_time} ~ ${this.activity.activity_end_time}`;
    },
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
      const activityIdHash = this.$route.params.activity_id_hash; // 从路由参数中获取活动 ID
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/activity/${activityIdHash}/`);
        this.activity = response.data;

        // 检查用户是否已报名
        const userId = localStorage.getItem('username'); // 假设用户 ID 存储在 localStorage 中
        const registrationsResponse = await axios.get(`http://127.0.0.1:8000/api/activity/${activityIdHash}/registrations/${userId}/`);
        if (registrationsResponse.data.length > 0) {
          this.hasRegistered = true;
        }
      } catch (error) {
        console.error("获取活动详情失败:", error);
      }
    },
    async registerForActivity() {
      const activityIdHash = this.$route.params.activity_id_hash; // 获取活动 ID
      try {
        const response = await axios.post(`http://127.0.0.1:8000/api/activity/register/${activityIdHash}/${localStorage.getItem('username')}/`);
        alert(response.data.message); // 显示成功消息
        this.hasRegistered = true; // 更新状态为已报名
        this.fetchActivityDetail(); // 重新获取活动详情以更新数据
      } catch (error) {
        if (error.response) {
          alert(error.response.data.error); // 显示错误消息
        } else {
          alert('报名失败，请稍后再试！');
          console.error("报名失败:", error);
        }
      }
    },
    navigateToReviseActivity() {
      this.$router.push({ name: 'ReviseActivity', params: { activity_id_hash: this.activity.activity_id } });
    },
    navigateToCheckVolunteer() {
      this.$router.push({ name: 'CheckVolunteer', params: { activity_id_hash: this.activity.activity_id } });
    },
  },
  mounted() {
    this.fetchActivityDetail();
  }
};
</script>

<style scoped>
.activity-detail-container {
  margin-top: 80px;
  padding: 2rem;
  background-color: #f0f2f5;
}

.activity-view {
  display: flex;
  width: 80%;
  margin: 0 auto;
  align-items: flex-start;
}

.activity-image {
  margin-top: 10px;
  width: 20%;
  height: 300px;
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
  width: 80%;
  margin: 0 auto;
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

<!-- 
    * @FileDescription: 活动详情页面，展示活动的详细信息 
    * @Author: infinity
    * @Date: 2024-10-24 
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-24
 -->

<template>
  <div>
    <NavBar />
    <div class="activity-detail-container">
      <div class="activity-view">
        <img :src="activity.image_path" alt="活动图片" class="activity-image" />
        <div class="activity-info">
          <h1 class="activity-title">{{ activity.activity_name }}</h1>
          <p class="activity-time">{{ activityPeriod }}</p>
          <div class="activity-details">
            <p v-if="activity.organizer">主办方: {{ activity.organizer }}</p>
            <p v-if="activity.contact_name">负责人姓名: {{ activity.contact_name }}</p>
            <p v-if="activity.contact_phone">负责人手机: {{ activity.contact_phone }}</p>
            <p v-if="activity.activity_tags">活动类型: {{ activity.activity_tags }}</p>
            <p v-if="activity.accepted_volunteers !== undefined">
              录取人数: {{ activity.accepted_volunteers }}
            </p>
            <p v-if="activity.estimated_volunteer_hours">劳动时长: {{ activity.estimated_volunteer_hours }}</p>
            <p v-if="registrationPeriod">报名时间: {{ registrationPeriod }}</p>
            <p v-if="activity.activity_location" class="activity-location">
              活动地点: {{ activity.activity_location }}
            </p>
            <button class="register-button" :disabled="isFull" @click="registerForActivity">
              {{ isFull ? '报名已满' : '报名' }}
            </button>
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
    };
  },
  computed: {
    /**
     * @description 判断活动是否已满员
     * @return {boolean} 是否满员
     */
    isFull() {
      return this.activity.accepted_volunteers >= this.activity.estimated_volunteer_hours;
    },
    activityPeriod() {
      return `${this.activity.activity_start_time} ~ ${this.activity.activity_end_time}`;
    },
    registrationPeriod() {
      return `${this.activity.application_start_time} ~ ${this.activity.application_end_time}`;
    },
  },
  methods: {
    async fetchActivityDetail() {
      const activityIdHash = this.$route.params.activity_id_hash; // 从路由参数中获取活动 ID
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/activities/${activityIdHash}/`);
        this.activity = response.data;
      } catch (error) {
        console.error("获取活动详情失败:", error);
      }
    },
    registerForActivity() {
      // 处理报名逻辑
      alert('报名成功！');
      // 此处可以增加更复杂的逻辑，比如调用后端API进行报名
    },
  },
  mounted() {
    console.log("Activity ID Hash:", this.$route.params.activity_id_hash); // 调试输出
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

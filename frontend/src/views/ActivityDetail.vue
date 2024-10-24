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
        <img :src="image" alt="活动图片" class="activity-image" />
        <div class="activity-info">
          <h1 class="activity-title">{{ title }}</h1>
          <p class="activity-time">{{ activityPeriod }}</p>
          <div class="activity-details">
            <!-- TODO 显示具体数据 -->
            <p v-if="host">主办方: {{ host }}</p>
            <p v-if="contactName">负责人姓名: {{ contactName }}</p>
            <p v-if="contactPhone">负责人手机: {{ contactPhone }}</p>
            <p v-if="label">活动类型: {{ label }}</p>
            <p v-if="participants">报名人数: {{ participants }}</p>
            <p v-if="registrationPeriod">报名时间: {{ registrationPeriod }}</p>
            <p v-if="location" class="activity-location">活动地点: {{ location }}</p>
            <button 
              class="register-button" 
              :disabled="isFull"
            >
              {{ isFull ? '报名已满' : '报名' }}
            </button>
          </div>
        </div>
      </div>
      <hr class="divider" />
      <div class="activity-description">
        <h2>活动描述</h2>
        <p>{{ activityDescription }}</p>
      </div>
      <div class="activity-notes">
        <h2>备注</h2>
        <p>{{ notes }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'ActivityDetailView',
  components: {
    NavBar,
  },
  data() {
    return {
      image: '../../activity-images/activity-1.jpg',
      title: '旋律欣赏活动1',
      host: '艺术学院',
      label: '劳动教育',
      participants: '60 / 60 人',
      registrationPeriod: '2024-10-12 ~ 2024-10-23',
      location: '图书馆',
      activityPeriod: '2024-10-10 ~ 2024-10-21',
      contactName: '张三',
      contactPhone: '1234567890',
      activityDescription: '这是一个旋律欣赏活动，旨在提高学生的音乐素养。',
      notes: '请准时参加活动。',
    };
  },
// TODO 从后端获取活动详情数据
  computed: {
    /** 
     * @description 判断活动是否已满员 
     * @return {boolean} 是否满员 
     */
    isFull() {
      return this.participants.split(' / ')[0] === this.participants.split(' / ')[1];
    }
  }
};
</script>

<style scoped>
/* TODO 调整样式 */
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
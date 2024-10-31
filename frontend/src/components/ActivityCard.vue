<!-- 
    * @FileDescription: 活动卡片组件，显示活动的图片、标题、主办方、报名人数、报名时间、地点和活动时间
    * @Author: infinity
    * @Date: 2024-10-29
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-29 
 -->

<template>
  <div class="activity-card" @click="goToDetail">
    <img :src="activity.activity_image_path" alt="活动图片" class="activity-image">
    <div class="activity-info">
      <h3>{{ activity.activity_name }}</h3>
      <p class="application-time">{{ formatDateTime(activity.application_start_time) }} - {{ formatDateTime(activity.application_end_time) }}</p>
      <p class="contact-name">{{ activity.organizer }}</p>
      <p class="accepted-volunteers">{{activity.registered_volunteers}} / {{ activity.accepted_volunteers }}人</p>
      <div class="bottom-info">
        <p class="activity-tags">{{ activity.activity_tags }}</p>
        <p class="activity-location">{{ activity.activity_location }}</p>
        <p class="activity-time">{{ formatDateTime(activity.activity_start_time) }} - {{ formatDateTime(activity.activity_end_time) }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ActivityCard',
  props: {
    activity: {
      type: Object,
      required: true,
    },
  },
  methods: {
    /**
     * @description 跳转到活动详情页面
     * @return {void}
     */
    goToDetail() {
      this.$router.push({ name: 'ActivityDetail', params: { activity_id_hash: this.activity.activity_id } });
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
};
</script>

<style scoped>
.activity-card {
  display: flex; 
  width: 380px;
  height: 220px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin: 10px;
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s;
}

.activity-card:hover {
  transform: scale(1.02);
}

.activity-image {
  width: 40%; 
  height: 100%; 
  object-fit: cover;
}

.activity-info {
  width: 60%; 
  padding: 5px;
  padding-left: 10px; 
  display: flex;
  flex-direction: column;
}

.activity-info h3 {
  font-size: 20px; 
  font-weight: bold; 
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis; 
}

.activity-info p {
  margin: 2px;
}

.application-time,
.activity-time {
  font-size: 12px; 
}

.contact-name,
.accepted-volunteers,
.activity-location {
  font-size: 14px; 
}

.contact-name,
.application-time,
.accepted-volunteers,
.activity-time,
.activity-location {
  color: #999; 
}

.activity-tags {
  color: orange; 
  margin: 0;
}

.activity-location {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis; 
}

.bottom-info {
  margin-top: auto; 
}
</style>
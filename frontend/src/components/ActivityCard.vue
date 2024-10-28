<!-- 
    * @FileDescription: 活动卡片组件，显示活动的图片、标题、主办方、报名人数、报名时间、地点和活动时间
    * @Author: infinity
    * @Date: 2024-10-22
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-22 
 -->

<template>
  <div class="activity-card" @click="goToDetail">
    <img :src="activity.activity_image_path" alt="活动图片" class="activity-image">
    <div class="activity-info">
      <h3>{{ activity.activity_name }}</h3>
      <p>主办方: {{ activity.contact_name }}</p>
      <p>标签: {{ activity.activity_tags }}</p>
      <p>报名人数: {{ activity.accepted_volunteers }}</p>
      <p>报名时间: {{ activity.application_start_time }} 至 {{ activity.application_end_time }}</p>
      <p>地点: {{ activity.activity_location }}</p>
      <p>活动时间: {{ activity.activity_start_time }} 至 {{ activity.activity_end_time }}</p>
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
    goToDetail() {
      this.$router.push({ name: 'ActivityDetail', params: { activity_id_hash: this.activity.activity_id } });
    },
  },

};
</script>

<style scoped>
.activity-card {
  display: block; /* 让整个卡片可点击 */
  width: 400px;
  height: 350px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: left;
  overflow: hidden;
  margin: 10px;
  text-decoration: none; /* 移除链接下划线 */
  color: inherit; /* 继承父元素的颜色 */
  transition: transform 0.2s; /* 添加过渡效果 */
}

.activity-card:hover {
  transform: scale(1.02); /* 悬停时稍微放大卡片 */
}

.activity-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.activity-info {
  padding: 15px;
}

.activity-info h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.activity-info p {
  font-size: 14px;
  margin-bottom: 5px;
}
</style>

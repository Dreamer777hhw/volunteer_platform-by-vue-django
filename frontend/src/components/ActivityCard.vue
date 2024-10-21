<!-- 
    * @FileDescription: 活动卡片组件，显示活动的图片、标题、主办方、报名人数、报名时间、地点和活动时间
    * @Author: infinity
    * @Date: 2024-10-21 
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-21 
 -->

<template>
  <div class="activity-card">
    <img :src="activity.image" alt="活动图片" class="activity-image">
    <div class="activity-info">
      <h3>{{ activity.title }}</h3>
      <p>主办方: {{ activity.host }}</p>
      <p>报名人数: {{ activity.participants }}</p>
      <p>报名时间: {{ activity.registrationPeriod }}</p>
      <p>地点: {{ activity.location }}</p>
      <p>活动时间: {{ activity.activityPeriod }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ActivityCard',
  props: {
    /**
     * @description 活动对象，包含活动的详细信息
     * @type {Object}
     * @required
     */
    activity: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
/* TODO 调整卡片样式 */
.activity-card {
  width: 30%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: left;
  overflow: hidden;
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
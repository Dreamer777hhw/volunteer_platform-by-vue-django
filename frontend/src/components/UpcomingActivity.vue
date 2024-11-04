<template>
  <div class="upcoming-activity-container">
    <h2>即将到来的活动</h2>
    <div class="upcoming-activity-list">
      <ActivityCard v-for="activity in activities"
                    :key="activity.activity_id"
                    :activity="activity" />
    </div>
  </div>
</template>

<script>
import ActivityCard from '@/components/ActivityCard.vue';

export default {
  name: 'UpcomingActivity',
  components: {
    ActivityCard,
  },
  props: {
    activities: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.upcoming-activity-container {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.upcoming-activity-list {
  display: flex;
  flex-wrap: wrap; /* 允许换行 */
}

.activity-card {
  margin: 10px; /* 每个卡片之间的间距 */
}
</style>

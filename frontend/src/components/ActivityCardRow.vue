<!-- 
    * @FileDescription: 活动卡片行组件，显示三个活动卡片在一行，间距固定
    * @Author: infinity
    * @Date: 2024-10-22 
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-22 
 -->

<template>
  <div class="activity-card-row">
    <ActivityCard v-for="(activity, index) in limitedActivities" :key="index" :activity="activity" />
  </div>
</template>

<script>
import ActivityCard from '@/components/ActivityCard.vue';

export default {
  name: 'ActivityCardRow',
  components: {
    ActivityCard,
  },
  props: {
    activities: {
      type: Array,
      required: true,
    },
  },
  computed: {
    /**
     * @description 返回前三个活动
     * @return {Array} 前三个活动
     */
    limitedActivities() {
      return this.activities.slice(0, 3);
    },
  },
};
</script>

<style scoped>
.activity-card-row {
  display: flex;
  width: 1200px;
  flex-wrap: nowrap; 
}
</style>
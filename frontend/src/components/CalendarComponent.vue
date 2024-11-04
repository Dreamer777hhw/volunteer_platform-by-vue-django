<template>
  <div class="calendar-layout">
    <!-- 日历部分 -->
    <div class="calendar-container">
      <div class="calendar-header">
        <button @click="previousMonth">«</button>
        <span>{{ currentYear }}年 {{ currentMonth + 1 }}月</span>
        <button @click="nextMonth">»</button>
      </div>
      <div class="calendar-grid">
        <div v-for="day in daysInMonth" :key="day.date" class="calendar-day" @click="selectDay(day)">
          <div class="day-content">
            <span class="day-number">{{ day.date }}</span>
            <span v-if="day.eventCount > 0" class="event-count">{{ day.eventCount }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 活动列表部分 -->
    <div class="event-list-container">
      <h3>活动列表</h3>
      <div v-if="selectedDayEvents.length > 0" class="event-list">
        <div class="event-list-slider">
          <ActivityCard
            v-for="event in selectedDayEvents"
            :key="event.activity_id"
            :activity="event"
            class="activity-card"
          />
        </div>
      </div>
      <div v-else class="no-events">该天无活动</div>
    </div>
  </div>
</template>



<script>
import ActivityCard from '@/components/ActivityCard.vue';
import axios from 'axios';

export default {
  name: 'CalendarComponent',
  components: { ActivityCard },
  data() {
    return {
      currentYear: new Date().getFullYear(),
      currentMonth: new Date().getMonth(),
      daysInMonth: [],
      activities: [],
      selectedDayEvents: [],
    };
  },
  async created() {
    await this.fetchActivities();
    this.generateCalendar();
  },
  methods: {
    async fetchActivities() {
      try {
        const start_date = new Date(this.currentYear, this.currentMonth, 1).toISOString().split('T')[0];
        const end_date = new Date(this.currentYear, this.currentMonth + 1, 0).toISOString().split('T')[0];

        const response = await axios.get('http://127.0.0.1:8000/api/calendar/', {
          params: { start_date, end_date },
        });
        this.activities = response.data;
        this.markEventDays();
      } catch (error) {
        console.error('Failed to load activities:', error);
      }
    },
    generateCalendar() {
      const daysInMonth = new Date(this.currentYear, this.currentMonth + 1, 0).getDate();
      this.daysInMonth = Array.from({ length: daysInMonth }, (_, i) => ({
        date: i + 1,
        eventCount: 0,
      }));
      this.markEventDays();
    },
    markEventDays() {
      this.activities.forEach(activity => {
        const activityDate = new Date(activity.activity_start_time);
        if (activityDate.getFullYear() === this.currentYear && activityDate.getMonth() === this.currentMonth) {
          const dayIndex = activityDate.getDate() - 1;
          this.daysInMonth[dayIndex].eventCount += 1;
        }
      });
    },
    selectDay(day) {
      const selectedDate = new Date(this.currentYear, this.currentMonth, day.date);
      this.selectedDayEvents = this.activities.filter(activity =>
        new Date(activity.activity_start_time).toDateString() === selectedDate.toDateString()
      );
    },
    previousMonth() {
      if (this.currentMonth === 0) {
        this.currentMonth = 11;
        this.currentYear--;
      } else {
        this.currentMonth--;
      }
      this.generateCalendar();
      this.fetchActivities();
    },
    nextMonth() {
      if (this.currentMonth === 11) {
        this.currentMonth = 0;
        this.currentYear++;
      } else {
        this.currentMonth++;
      }
      this.generateCalendar();
      this.fetchActivities();
    },
  },
};
</script>

<style scoped>
.calendar-layout {
  display: flex;
  gap: 24px; /* 间距 */
  padding: 16px;
}

.calendar-container {
  width: 50%;
  max-width: 400px;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  padding: 10px 20px;
  background-color: #f4f4f4;
  font-weight: bold;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background-color: #ddd;
}

.calendar-day {
  position: relative;
  background-color: #fff;
  min-height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.day-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.day-number {
  font-size: 18px;
  font-weight: bold;
}

.event-count {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: #f56c6c;
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 12px;
  font-weight: bold;
}

.event-list-container {
  width: 100%;
  max-width: 800px; /* 调整容器宽度以适应两个卡片 */
  overflow-x: auto;
}

.event-list {
  margin-top: 10px;
  padding: 30px;
  overflow-x: auto; /* 横向滚动 */
  white-space: nowrap;
}

.event-list-slider {
  display: flex;
  gap: 16px;
  overflow-x: scroll;
  padding: 8px;
}

.event-list-slider > * {
  flex: 0 0 380px; /* 固定每个活动卡片的宽度 */
  max-width: 500px;
  height: 220px; /* 保持高度 */
  display: inline-block;
}

.no-events {
  padding: 10px;
  color: #999;
  text-align: center;
}
.activity-card {
  min-width: 350px; /* 调整单个卡片的最小宽度 */
  flex: 1;
}

.activity-image {
  width: 40%;
  height: auto;
  object-fit: cover;
}

.activity-info {
  width: 60%;
  padding: 5px;
  padding-left: 10px;
  display: flex;
  flex-direction: column;
}

</style>

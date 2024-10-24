<!-- 
    * @FileDescription: 检查志愿者申请页面，用户可以在此页面查看和管理志愿者申请 
    * @Author: infinity
    * @Date: 2024-10-24 
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-24
 -->

<template>
  <div>
    <NavBar />
    <div class="check-volunteer-container">
      <div class="check-volunteer-card">
        <h2 class="check-volunteer-title">检查志愿者申请</h2>
        <div class="activity-name">
          <label>活动名称：</label>
          <span>{{ activityName }}</span>
        </div>
        <div class="volunteer-list-header">
          <span>姓名</span>
          <span>学号</span>
          <span>专业</span>
          <span>学院</span>
          <span>邮箱</span>
          <span>手机号</span>
          <span>操作</span>
        </div>
        <div class="volunteer-list">
          <div v-for="volunteer in volunteers" :key="volunteer.id" class="volunteer-row">
            <span>{{ volunteer.name }}</span>
            <span>{{ volunteer.studentId }}</span>
            <span>{{ volunteer.major }}</span>
            <span>{{ volunteer.college }}</span>
            <span>{{ volunteer.email }}</span>
            <span>{{ volunteer.phone }}</span>
            <div class="action-buttons">
              <button @click="approveVolunteer(volunteer.id)">同意</button>
              <button @click="rejectVolunteer(volunteer.id)">拒绝</button>
            </div>
          </div>
        </div>
        <div class="bulk-action-buttons">
          <button @click="approveAll">一键同意</button>
          <button @click="rejectAll">一键拒绝</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
  name: 'CheckVolunteerView',
  components: {
    NavBar,
  },
  data() {
    return {
      activityId: 'fixed_hash_value', 
      activityName: '示例活动名称',
      volunteers: [
        { id: 1, name: '张三', studentId: '20210001', major: '计算机科学', college: '信息学院', email: 'zhangsan@example.com', phone: '12345678901' },
        { id: 2, name: '李四', studentId: '20210002', major: '软件工程', college: '信息学院', email: 'lisi@example.com', phone: '12345678902' },
        { id: 3, name: '王五', studentId: '20210003', major: '网络工程', college: '信息学院', email: 'wangwu@example.com', phone: '12345678903' },
        // 其他志愿者数据
      ],
    };
  },
  methods: {
    /** 
     * @description 同意志愿者申请 
     * @param {number} id - 志愿者ID 
     * @return {void}
     */
    approveVolunteer(id) {
      // TODO: 同意志愿者申请逻辑
      console.log(`同意志愿者申请: ${id}`);
    },
    /** 
     * @description 拒绝志愿者申请 
     * @param {number} id - 志愿者ID 
     * @return {void}
     */
    rejectVolunteer(id) {
      // TODO: 拒绝志愿者申请逻辑
      console.log(`拒绝志愿者申请: ${id}`);
    },
    /** 
     * @description 一键同意所有志愿者申请 
     * @return {void}
     */
    approveAll() {
      // TODO: 一键同意所有志愿者申请逻辑
      console.log('一键同意所有志愿者申请');
    },
    /** 
     * @description 一键拒绝所有志愿者申请 
     * @return {void}
     */
    rejectAll() {
      // TODO: 一键拒绝所有志愿者申请逻辑
      console.log('一键拒绝所有志愿者申请');
    }
  }
};
</script>

<style scoped>
/* TODO 修改样式 */
.check-volunteer-container {
  background-color: #f0f2f5;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.check-volunteer-card {
  margin-top: 80px;
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 1000px;
}

.check-volunteer-title {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.activity-name {
  margin-bottom: 1rem;
}

.volunteer-list-header,
.volunteer-row {
  display: grid;
  grid-template-columns: 100px 100px 150px 150px 200px 150px 150px;
  padding: 10px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
}

.volunteer-list-header {
  font-weight: bold;
}

.volunteer-row {
  background-color: white;
  border-top: none;
}

.volunteer-row span,
.volunteer-list-header span {
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.action-buttons {
  display: flex;
  justify-content: space-around;
}

.bulk-action-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.bulk-action-buttons button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>
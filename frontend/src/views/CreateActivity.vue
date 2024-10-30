<!-- 
    * @FileDescription: 创建活动页面，用户可以在此页面创建新的活动 
    * @Author: infinity
    * @Date: 2024-10-24 
    * @LastEditors: dreamer777hhw
    * @LastEditTime: 2024-10-30
 -->

<template>
<div>
  <NavBar />
  <div class="create-activity-container">
    <div class="create-activity-card">
      <h2 class="create-activity-title">创建活动</h2>
      <form @submit.prevent="createActivity">
        <div class="input-group">
          <div class="input-field">
            <label>活动名称：</label>
            <input
              type="text"
              v-model="activityName"
              required
            />
          </div>
          <div class="input-field">
            <label>活动描述：</label>
            <textarea
              v-model="activityDescription"
              required
            ></textarea>
          </div>
          <div class="input-field">
            <label>选择活动标签：</label>
            <select v-model="activityTag" required>
              <option value="" disabled selected>选择活动标签</option>
              <option v-for="(label, value) in activityTags" :key="value" :value="value">{{ label }}</option>
            </select>
          </div>
          <div class="input-field">
            <label>上传图片：</label>
            <input
              type="file"
              @change="uploadPic"
              required
            />
          </div>
          <div class="input-field">
            <label>报名要求：</label>
            <textarea
              v-model="applicationRequirements"
              required
            ></textarea>
          </div>
          <div class="input-field">
            <label>报名开始时间：</label>
            <input
              type="datetime-local"
              v-model="applicationStartTime"
              required
            />
          </div>
          <div class="input-field">
            <label>报名结束时间：</label>
            <input
              type="datetime-local"
              v-model="applicationEndTime"
              required
            />
          </div>
          <div class="input-field">
            <label>活动开始时间：</label>
            <input
              type="datetime-local"
              v-model="activityStartTime"
              required
            />
          </div>
          <div class="input-field">
            <label>活动结束时间：</label>
            <input
              type="datetime-local"
              v-model="activityEndTime"
              required
            />
          </div>
          <div class="input-field">
            <label>预计志愿时长：</label>
            <input
              type="number"
              v-model="volunteerHours"
              required
            />
          </div>
          <div class="input-field">
            <label>活动地点：</label>
            <input
              type="text"
              v-model="activityLocation"
              required
            />
          </div>
          <div class="input-field">
            <label>联系人姓名：</label>
            <input
              type="text"
              v-model="contactName"
              required
            />
          </div>
          <div class="input-field">
            <label>联系人电话：</label>
            <input
              type="text"
              v-model="contactPhone"
              required
            />
          </div>
          <div class="input-field">
            <label>招募人数：</label>
            <input
              type="number"
              v-model="acceptedVolunteers"
              required
            />
          </div>
          <div class="input-field">
            <label>劳动学时：</label>
            <input
              type="number"
              v-model="laborHours"
              required
            />
          </div>
          <div class="input-field">
            <label>素拓：</label>
            <input
              type="text"
              v-model="sutuo"
              required
            />
          </div>
          <div class="input-field">
            <label>备注：</label>
            <textarea
              v-model="notes"
              required
            ></textarea>
          </div>
        </div>
        <button class="create-activity-button" type="submit">创建活动</button>
      </form>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

export default {
  name: 'CreateActivityView',
  components: {
    NavBar,
  },
  data() {
    return {
      activityName: '',
      activityDescription: '',
      activityTag: '',
      applicationRequirements: '',
      applicationStartTime: '',
      applicationEndTime: '',
      activityStartTime: '',
      activityEndTime: '',
      volunteerHours: '',
      activityLocation: '',
      contactName: '',
      contactPhone: '',
      acceptedVolunteers: '',
      laborHours: '',
      sutuo: '',
      notes: '',
      activityTags: {
        '讲坛讲座': '讲坛讲座',
        '志愿公益': '志愿公益',
        '劳动教育': '劳动教育',
        '文体活动': '文体活动',
        '实习实践': '实习实践',
        '学习培训': '学习培训',
        '科创活动': '科创活动',
      },
      imageUrl: '', // 保存上传图片的URL
    };
  },
  methods: {
    /**
     * @description 上传图片
     * @param {Event} event - 文件选择事件
     * @return {void}
     */
    async uploadPic(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await axios.post('http://127.0.0.1:8000/api/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        this.imageUrl = response.data.url; // 假设返回的图片 URL 在 response.data.url 中
      } catch (error) {
        console.error('图片上传失败:', error);
      }
    },

    /**
     * @description 创建活动
     * @return {void}
     */
    async createActivity() {
      const payload = {
        activity_name: this.activityName,
        activity_description: this.activityDescription,
        activity_tags: this.activityTag,
        application_requirements: this.applicationRequirements,
        application_start_time: this.applicationStartTime,
        application_end_time: this.applicationEndTime,
        activity_start_time: this.activityStartTime,
        activity_end_time: this.activityEndTime,
        estimated_volunteer_hours: this.volunteerHours,
        activity_location: this.activityLocation,
        contact_name: this.contactName,
        contact_phone: this.contactPhone,
        accepted_volunteers: this.acceptedVolunteers,
        labor_hours: this.laborHours,
        sutuo: this.sutuo,
        notes: this.notes,
        activity_image_path: this.imageUrl, // 使用上传的图片 URL
        organizer: localStorage.getItem('username'), // 使用当前登录用户的用户名
      };

      try {
        const response = await axios.post('http://127.0.0.1:8000/api/activities/', payload);
        console.log('活动创建成功:', response.data);
        this.$router.push('/'); // 跳转到活动页面
      } catch (error) {
        console.error('活动创建失败:', error);
      }
    },
  },
};
</script>

<style scoped>
/* 样式保持不变 */
.create-activity-container {
  background-color: #f0f2f5;
  display: flex;
  justify-content: center;
  align-items: center;
}

.create-activity-card {
  margin-top: 80px;
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 300px;
}

.create-activity-title {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-field {
  margin-bottom: 1rem;
}

.input-field label {
  display: block;
  margin-bottom: 0.5rem;
}

.input-field input,
.input-field select,
.input-field textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.create-activity-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>
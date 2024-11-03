<!-- 
    * @FileDescription: 修改活动页面，用户可以在此页面修改当前活动 
    * @Author: infinity
    * @Date: 2024-10-24 
    * @LastEditors: infinity 
    * @LastEditTime: 2024-10-24
 -->

<template>
  <div class="container">
    <NavBar />
    <div class="create-activity-container">
      <div class="create-activity-card">
        <h2 class="create-activity-title">修改活动</h2>
        <form @submit.prevent="reviseActivity">
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
              <label>当前活动图片：</label>
              <img v-if="activityImagePath" :src="activityImagePath" alt="活动图片" class="activity-image" />
            </div>
            <div class="input-field">
              <label>上传图片：</label>
              <input
                type="file"
                @change="uploadPic"
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
              <span v-if="errors.applicationStartTime" class="error">{{ errors.applicationStartTime }}</span>
            </div>
            <div class="input-field">
              <label>报名结束时间：</label>
              <input
                type="datetime-local"
                v-model="applicationEndTime"
                required
              />
              <span v-if="errors.applicationEndTime" class="error">{{ errors.applicationEndTime }}</span>
            </div>
            <div class="input-field">
              <label>活动开始时间：</label>
              <input
                type="datetime-local"
                v-model="activityStartTime"
                required
              />
              <span v-if="errors.activityStartTime" class="error">{{ errors.activityStartTime }}</span>
            </div>
            <div class="input-field">
              <label>活动结束时间：</label>
              <input
                type="datetime-local"
                v-model="activityEndTime"
                required
              />
              <span v-if="errors.activityEndTime" class="error">{{ errors.activityEndTime }}</span>
            </div>
            <div class="input-field">
              <label>预计志愿时长：</label>
              <input
                type="number"
                v-model="volunteerHours"
                required
              />
              <span v-if="errors.volunteerHours" class="error">{{ errors.volunteerHours }}</span>
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
              <span v-if="errors.acceptedVolunteers" class="error">{{ errors.acceptedVolunteers }}</span>
            </div>
            <div class="input-field">
              <label>劳动学时：</label>
              <input
                type="number"
                v-model="laborHours"
                required
              />
              <span v-if="errors.laborHours" class="error">{{ errors.laborHours }}</span>
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
          <button class="create-activity-button" type="submit">修改活动</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';

export default {
  name: 'ReviseActivityView',
  components: {
    NavBar,
  },
  data() {
    return {
      activityId: '',
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
      activityImagePath: '',
      activityTags: {
        '讲坛讲座': '讲坛讲座',
        '志愿公益': '志愿公益',
        '劳动教育': '劳动教育',
        '文体活动': '文体活动',
        '实习实践': '实习实践',
        '学习培训': '学习培训',
        '科创活动': '科创活动',
      },
      errors: {
        applicationStartTime: '',
        applicationEndTime: '',
        activityStartTime: '',
        activityEndTime: '',
        acceptedVolunteers: '',
        volunteerHours: '',
        laborHours: '',
      },
    };
  },
  created() {
    this.activityId = this.$route.params.activity_id_hash; // 从路由获取活动ID
    this.fetchActivityDetails();
  },
  watch: {
    applicationStartTime(value) {
      this.validateApplicationStartTime(value);
    },
    applicationEndTime(value) {
      this.validateApplicationEndTime(value);
    },
    activityStartTime(value) {
      this.validateActivityStartTime(value);
    },
    activityEndTime(value) {
      this.validateActivityEndTime(value);
    },
    acceptedVolunteers(value) {
      this.validateAcceptedVolunteers(value);
    },
    volunteerHours(value) {
      this.validateVolunteerHours(value);
    },
    laborHours(value) {
      this.validateLaborHours(value);
    },
  },
  methods: {
    /**
     * @description 格式化日期时间
     * @param {string} dateTime 日期时间字符串
     * @return {string} 格式化后的日期时间字符串
     */
    formatDateTime(dateTime) {
      if (!dateTime) return '';
      const date = new Date(dateTime);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从0开始
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${year}-${month}-${day}T${hours}:${minutes}`;
    },
    /**
     * @description 获取活动详情
     * @return {void}
     */
    async fetchActivityDetails() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/reviseactivity/${this.activityId}/`);
        const activity = response.data;
        // 将活动详情填充到数据模型
        this.activityName = activity.activity_name;
        this.activityDescription = activity.activity_description;
        this.activityTag = activity.activity_tags;
        this.applicationRequirements = activity.application_requirements;
        this.applicationStartTime = this.formatDateTime(activity.application_start_time);
        this.applicationEndTime = this.formatDateTime(activity.application_end_time);
        this.activityStartTime = this.formatDateTime(activity.activity_start_time);
        this.activityEndTime = this.formatDateTime(activity.activity_end_time);
        this.volunteerHours = activity.estimated_volunteer_hours;
        this.activityLocation = activity.activity_location;
        this.contactName = activity.contact_name;
        this.contactPhone = activity.contact_phone;
        this.acceptedVolunteers = activity.accepted_volunteers;
        this.laborHours = activity.labor_hours;
        this.sutuo = activity.sutuo;
        this.notes = activity.notes;
        this.activityImagePath = activity.activity_image_path;
      } catch (error) {
        console.error("获取活动详情失败:", error);
      }
    },
    /**
     * @description 上传图片
     * @param {Event} event 文件选择事件
     * @return {void}
     */
    uploadPic(event) {
      const file = event.target.files[0];
      if (file) {
        const formData = new FormData();
        formData.append('activity_name', this.activityName); // 将活动名称添加到表单数据中
        formData.append('file', file); // 将文件添加到表单数据中

        axios.post('http://127.0.0.1:8000/api/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        })
        .then(response => {
          this.activityImagePath = response.data.url; // 更新活动图片路径
        })
        .catch(error => {
          console.error('上传图片失败:', error);
          alert('上传图片失败，请稍后再试！');
        });
      }
    },
    /**
     * @description 验证报名开始时间
     * @param {string} value 报名开始时间
     * @return {void}
     */
    validateApplicationStartTime(value) {
      const now = new Date().toISOString();
      if (value <= now) {
        this.errors.applicationStartTime = '报名开始时间应晚于当前时间';
      } else {
        this.errors.applicationStartTime = '';
      }
    },
    /**
     * @description 验证报名结束时间
     * @param {string} value 报名结束时间
     * @return {void}
     */
    validateApplicationEndTime(value) {
      if (value <= this.applicationStartTime) {
        this.errors.applicationEndTime = '报名结束时间应晚于报名开始时间';
      } else {
        this.errors.applicationEndTime = '';
      }
    },
    /**
     * @description 验证活动开始时间
     * @param {string} value 活动开始时间
     * @return {void}
     */
    validateActivityStartTime(value) {
      if (value <= this.applicationEndTime) {
        this.errors.activityStartTime = '活动开始时间应晚于报名结束时间';
      } else {
        this.errors.activityStartTime = '';
      }
    },
    /**
     * @description 验证活动结束时间
     * @param {string} value 活动结束时间
     * @return {void}
     */
    validateActivityEndTime(value) {
      if (value <= this.activityStartTime) {
        this.errors.activityEndTime = '活动结束时间应晚于活动开始时间';
      } else {
        this.errors.activityEndTime = '';
      }
    },
    /**
     * @description 验证招募人数
     * @param {number} value 招募人数
     * @return {void}
     */
    validateAcceptedVolunteers(value) {
      if (value < 0) {
        this.errors.acceptedVolunteers = '招募人数应大于等于0';
      } else {
        this.errors.acceptedVolunteers = '';
      }
    },
    /**
     * @description 验证预计志愿时长
     * @param {number} value 预计志愿时长
     * @return {void}
     */
    validateVolunteerHours(value) {
      if (value < 0) {
        this.errors.volunteerHours = '预计志愿时长应大于等于0';
      } else {
        this.errors.volunteerHours = '';
      }
    },
    /**
     * @description 验证劳动学时
     * @param {number} value 劳动学时
     * @return {void}
     */
    validateLaborHours(value) {
      if (value < 0) {
        this.errors.laborHours = '劳动学时应大于等于0';
      } else {
        this.errors.laborHours = '';
      }
    },
    /**
     * @description 清除错误信息
     * @return {void}
     */
    clearErrors() {
      this.errors = {
        applicationStartTime: '',
        applicationEndTime: '',
        activityStartTime: '',
        activityEndTime: '',
        acceptedVolunteers: '',
        volunteerHours: '',
        laborHours: '',
      };
    },
    /**
     * @description 验证所有输入
     * @return {boolean} 是否通过验证
     */
    validateInputs() {
      this.validateApplicationStartTime(this.applicationStartTime);
      this.validateApplicationEndTime(this.applicationEndTime);
      this.validateActivityStartTime(this.activityStartTime);
      this.validateActivityEndTime(this.activityEndTime);
      this.validateAcceptedVolunteers(this.acceptedVolunteers);
      this.validateVolunteerHours(this.volunteerHours);
      this.validateLaborHours(this.laborHours);

      return !Object.values(this.errors).some(error => error !== '');
    },
    /**
     * @description 修改活动
     * @return {void}
     */
    async reviseActivity() {
      this.clearErrors();
      if (!this.validateInputs()) {
        return;
      }
      try {
        const updatedActivity = {
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
        };
        const response = await axios.put(`http://127.0.0.1:8000/api/reviseactivity/${this.activityId}/`, updatedActivity);
        alert('活动修改成功！');
        this.$router.push(`/activity/detail/${this.activityId}`);
        console.log('修改活动成功:', response.data);

      } catch (error) {
        console.error("修改活动失败:", error);
        alert('修改活动失败，请稍后再试！');
      }
    }
  }
};
</script>

<style scoped>
.create-activity-container {
  background-image: url('../../public/background/bg.webp');
  background-repeat: repeat;
  background-size: auto;
  background-position: center;
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

.error {
  color: red;
  font-size: 0.875rem;
}

.activity-image {
  max-width: 100%;
  height: auto;
  border-radius: 5px;
  margin-top: 0.5rem;
}
</style>
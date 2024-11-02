<!--
    * @FileDescription: 修改信息页面组件，包含姓名、学院、专业、邮箱、手机号等输入框，并进行相应的验证
    * @Author: Dreamer777hhw
    * @Date: 2024-10-23
    * @LastEditors: dreamer777hhw
    * @LastEditTime: 2024-11-02
    *



 -->
<template>
<div>
  <NavBar/>
  <div class="modify-info-container">
    <div class="info-card">
      <h2>修改信息</h2>
      <div class="info-item">
        <span class="info-label">姓名：</span>
        <input v-model="editName" type="text" />
      </div>
      <div class="info-item">
        <span class="info-label">学院：</span>
        <select v-model="editSchool">
          <option value="" disabled selected>选择学院</option>
          <option v-for="(label, value) in schools" :key="value" :value="value">{{ label }}</option>
        </select>
      </div>
      <div class="info-item">
        <span class="info-label">专业：</span>
        <input v-model="editMajor" type="text" />
      </div>
      <div class="info-item">
        <span class="info-label">邮箱：</span>
        <input v-model="editEmail" type="email" />
      </div>
      <div class="info-item">
        <span class="info-label">手机号：</span>
        <input v-model="editPhone" type="text" />
      </div>
      <button @click="submitInfoChange">提交修改</button>
    </div>
  </div>
</div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';

export default {
  name: 'ModifyInfoView',
  components: {
    NavBar,
  },
  data() {
    return {
      editName: this.$route.query.name || '',
      editSchool: this.$route.query.school || '',
      editMajor: this.$route.query.major || '',
      editEmail: this.$route.query.email || '',
      editPhone: this.$route.query.phone || '',
      schools: {
        '工科': '工科',
        '船舶海洋与建筑工程学院': '船舶海洋与建筑工程学院',
        '机械与动力工程学院': '机械与动力工程学院',
        '电子信息与电气工程学院': '电子信息与电气工程学院',
        '集成电路学院': '集成电路学院',
        '材料科学与工程学院': '材料科学与工程学院',
        '环境科学与工程学院': '环境科学与工程学院',
        '生物医学工程学院': '生物医学工程学院',
        '航空航天学院': '航空航天学院',
        '理科': '理科',
        '数学科学学院': '数学科学学院',
        '物理与天文学院': '物理与天文学院',
        '化学化工学院': '化学化工学院',
        '海洋学院': '海洋学院',
        '生命科学': '生命科学',
        '生命科学技术学院': '生命科学技术学院',
        '农业与生物学院': '农业与生物学院',
        '医学院': '医学院',
        '药学院': '药学院',
        '人文社科': '人文社科',
        '安泰经济与管理学院': '安泰经济与管理学院',
        '凯原法学院': '凯原法学院',
        '外国语学院': '外国语学院',
        '人文学院': '人文学院',
        '马克思主义学院': '马克思主义学院',
        '国际与公共事务学院': '国际与公共事务学院',
        '媒体与传播学院': '媒体与传播学院',
        '设计学院': '设计学院',
        '体育系': '体育系',
        '上海高级金融学院': '上海高级金融学院',
        '国际化办学': '国际化办学',
        '上海交大密西根学院': '上海交大密西根学院',
        '巴黎卓越工程师学院': '巴黎卓越工程师学院',
        '上海交大-南加州大学文化创意产业学院': '上海交大-南加州大学文化创意产业学院',
        '中欧国际工商学院': '中欧国际工商学院',
        '中英国际低碳学院': '中英国际低碳学院',
        '交叉学科': '交叉学科',
        '致远学院': '致远学院',
        '智慧能源创新学院': '智慧能源创新学院',
        '教育学院': '教育学院',
        '溥渊未来技术学院': '溥渊未来技术学院',
        '人工智能学院': '人工智能学院',
        '心理学院': '心理学院',
        '研究院·基础研究': '研究院·基础研究',
        '系统生物医学研究院': '系统生物医学研究院',
        '自然科学研究院': '自然科学研究院',
        '海洋研究院': '海洋研究院',
        '李政道研究所': '李政道研究所',
        '中国法与社会研究院': '中国法与社会研究院',
        '变革性分子前沿科学中心': '变革性分子前沿科学中心',
        '张江高等研究院': '张江高等研究院',
        '研究院·应用基础研究': '研究院·应用基础研究',
        '能源研究院': '能源研究院',
        '空天科学技术研究院': '空天科学技术研究院',
        '汽车工程研究院': '汽车工程研究院',
        '航空发动机研究院': '航空发动机研究院',
        '燃气轮机研究院': '燃气轮机研究院',
        '上海智能制造研究院': '上海智能制造研究院',
        '医疗机器人研究院': '医疗机器人研究院',
        '医学影像先进技术研究院': '医学影像先进技术研究院',
        '人工智能研究院': '人工智能研究院',
        '三亚崖州湾深海科技研究院': '三亚崖州湾深海科技研究院',
        '元知机器人研究院': '元知机器人研究院',
        '研究院·综合交叉': '研究院·综合交叉',
        '碳中和发展研究院': '碳中和发展研究院',
        'Bio-X研究院': 'Bio-X研究院',
        'Med-X研究院': 'Med-X研究院',
        '转化医学研究院': '转化医学研究院',
        '个性化医学研究院': '个性化医学研究院',
        '董浩云航运与物流研究院（中美物流研究院）': '董浩云航运与物流研究院（中美物流研究院）',
        '新农村发展研究院（农业与生物学院）': '新农村发展研究院（农业与生物学院）'
      },
    };
  },
  methods: {
    /**
     * @description 提交修改后的信息
     * @return {void}
     */
    async submitInfoChange() {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('未找到token，无法修改信息！');
        return;
      }

      try {
        const response = await axios.post(`http://127.0.0.1:8000/api/account-update/`, {
          name: this.editName,
          school: this.editSchool,
          major: this.editMajor,
          email: this.editEmail,
          phone: this.editPhone,
          student_id: localStorage.getItem('username'),
        },);
        if (response.status === 200) {
          alert('信息修改成功！');
          this.$router.push('/account'); // Navigate back to the account page
        }
      } catch (error) {
        console.error("修改信息失败:", error);
        alert('信息修改失败，请重试！');
      }
    }
  }
};
</script>

<style scoped>
.modify-info-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90vh;
  background-color: #f0f2f5;
  padding: 2rem;
}

.info-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 300px;
}

.info-item {
  margin-bottom: 1rem;
}
</style>

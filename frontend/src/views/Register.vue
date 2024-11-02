<!-- 
    * @FileDescription: 注册页面组件，包含学号、姓名、学院、专业、邮箱、手机号、密码等输入框，并进行相应的验证
    * @Author: infinity 
    * @Date: 2024-10-29 
    * @LastEditors: infinity
    * @LastEditTime: 2024-10-29
 -->

<template>
  <div class="register-container">
    <div class="register-card">
      <h2 class="register-title">注册</h2>
      <form @submit.prevent="register">
        <div class="input-group">
          <div class="input-field">
            <input
              type="text"
              v-model="studentId"
              placeholder="学号（12位数字）"
              required
              @input="validateStudentId"
            />
            <span v-if="studentIdError" class="error-message">{{ studentIdError }}</span>
          </div>
          <div class="input-field">
            <input
              type="text"
              v-model="name"
              placeholder="姓名"
              required
            />
          </div>
          <div class="input-field">
            <select v-model="school" required>
              <option value="" disabled selected>选择学院</option>
              <option v-for="(label, value) in schools" :key="value" :value="value">{{ label }}</option>
            </select>
          </div>
          <div class="input-field">
            <input
              type="text"
              v-model="major"
              placeholder="专业"
              required
            />
          </div>
          <div class="input-field">
            <input
              type="email"
              v-model="email"
              placeholder="邮箱（@sjtu.edu.cn结尾）"
              required
              @input="validateEmail"
            />
            <span v-if="emailError" class="error-message">{{ emailError }}</span>
          </div>
          <div class="input-field">
            <input
              type="text"
              v-model="phone"
              placeholder="手机号"
              required
            />
          </div>
          <div class="input-field">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="密码"
              required
            />
          </div>
          <div class="input-field">
            <input
              :type="showConfirmPassword ? 'text' : 'password'"
              v-model="confirmPassword"
              placeholder="确认密码"
              required
              @input="validatePassword"
            />
            <span v-if="passwordError" class="error-message">{{ passwordError }}</span>
          </div>
          <div v-if="registerError" class="register-error">{{ registerError }}</div>
        </div>
        <button class="register-button" type="submit">确认注册</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'RegisterView',
  data() {
    return {
      studentId: '',
      name: '',
      school: '',
      major: '',
      email: '',
      phone: '',
      password: '',
      confirmPassword: '',
      studentIdError: '',
      emailError: '',
      passwordError: '',
      registerError: '',
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
      }
    };
  },
  methods: {
    /**
     * @description 验证学号格式是否正确
     * @return {void}
     */
    validateStudentId() {
      const studentIdPattern = /^\d{12}$/;
      this.studentIdError = studentIdPattern.test(this.studentId) ? '' : '学号必须是12位数字';
    },
    /**
     * @description 验证邮箱格式是否正确
     * @return {void}
     */
    validateEmail() {
      const emailPattern = /^[a-zA-Z0-9._%+-]+@sjtu\.edu\.cn$/;
      this.emailError = emailPattern.test(this.email) ? '' : '邮箱必须以@sjtu.edu.cn结尾';
    },
    /**
     * @description 验证两次输入的密码是否一致
     * @return {void}
     */
    validatePassword() {
      this.passwordError = this.password === this.confirmPassword ? '' : '两次输入的密码不一致';
    },
    /**
     * @description 注册方法，验证输入信息并存储到 localStorage
     * @return {void}
     */
    async register() {
      this.validateStudentId();
      this.validateEmail();
      this.validatePassword();

      if (!this.studentIdError && !this.emailError && !this.passwordError) {
        try {
          const response = await axios.post('http://127.0.0.1:8000/api/register/', {
            student_id: this.studentId,
            name: this.name,
            school: this.school,
            major: this.major,
            email: this.email,
            phone: this.phone,
            password: this.password,
          });

          if (response.status === 201) {
            // alert(response.data.message);
            this.$router.push({path: '/login'});
          }
        } catch (error) {
          if (error.response && error.response.data) {
            // alert("注册失败: " + JSON.stringify(error.response.data));
            this.registerError = error.response.data.message + ", 请重试";
          } else {
            // alert("注册失败: 网络错误");
            this.registerError = "网络错误，请重试";
          }
        }
      }
    },
  },
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
  background-image: url('../../public/background/background1.jpg');
  background-size: cover;
  background-position: center;
}

.register-card {
  background: white;
  padding-bottom: 2rem;
  padding-left: 3rem;
  padding-right: 3rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 300px;
}

.register-title {
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

.input-field input,
.input-field select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

.error-message {
  color: red;
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

.register-error {
  color: red;
  font-size: 0.875rem;
  margin-top: -0.5rem;
  margin-bottom: 1rem;
}

.register-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
</style>
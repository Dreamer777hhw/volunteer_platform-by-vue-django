from django.db import models
from django.contrib.auth.hashers import make_password, check_password

SCHOOL_CHOICES = [
    ('工科', '工科'),
    ('船舶海洋与建筑工程学院', '船舶海洋与建筑工程学院'),
    ('机械与动力工程学院', '机械与动力工程学院'),
    ('电子信息与电气工程学院', '电子信息与电气工程学院'),
    ('集成电路学院', '集成电路学院'),
    ('材料科学与工程学院', '材料科学与工程学院'),
    ('环境科学与工程学院', '环境科学与工程学院'),
    ('生物医学工程学院', '生物医学工程学院'),
    ('航空航天学院', '航空航天学院'),
    ('理科', '理科'),
    ('数学科学学院', '数学科学学院'),
    ('物理与天文学院', '物理与天文学院'),
    ('化学化工学院', '化学化工学院'),
    ('海洋学院', '海洋学院'),
    ('生命科学', '生命科学'),
    ('生命科学技术学院', '生命科学技术学院'),
    ('农业与生物学院', '农业与生物学院'),
    ('医学院', '医学院'),
    ('药学院', '药学院'),
    ('人文社科', '人文社科'),
    ('安泰经济与管理学院', '安泰经济与管理学院'),
    ('凯原法学院', '凯原法学院'),
    ('外国语学院', '外国语学院'),
    ('人文学院', '人文学院'),
    ('马克思主义学院', '马克思主义学院'),
    ('国际与公共事务学院', '国际与公共事务学院'),
    ('媒体与传播学院', '媒体与传播学院'),
    ('设计学院', '设计学院'),
    ('体育系', '体育系'),
    ('上海高级金融学院', '上海高级金融学院'),
    ('国际化办学', '国际化办学'),
    ('上海交大密西根学院', '上海交大密西根学院'),
    ('巴黎卓越工程师学院', '巴黎卓越工程师学院'),
    ('上海交大-南加州大学文化创意产业学院', '上海交大-南加州大学文化创意产业学院'),
    ('中欧国际工商学院', '中欧国际工商学院'),
    ('中英国际低碳学院', '中英国际低碳学院'),
    ('交叉学科', '交叉学科'),
    ('致远学院', '致远学院'),
    ('智慧能源创新学院', '智慧能源创新学院'),
    ('教育学院', '教育学院'),
    ('溥渊未来技术学院', '溥渊未来技术学院'),
    ('人工智能学院', '人工智能学院'),
    ('心理学院', '心理学院'),
    ('研究院·基础研究', '研究院·基础研究'),
    ('系统生物医学研究院', '系统生物医学研究院'),
    ('自然科学研究院', '自然科学研究院'),
    ('海洋研究院', '海洋研究院'),
    ('李政道研究所', '李政道研究所'),
    ('中国法与社会研究院', '中国法与社会研究院'),
    ('变革性分子前沿科学中心', '变革性分子前沿科学中心'),
    ('张江高等研究院', '张江高等研究院'),
    ('研究院·应用基础研究', '研究院·应用基础研究'),
    ('能源研究院', '能源研究院'),
    ('空天科学技术研究院', '空天科学技术研究院'),
    ('汽车工程研究院', '汽车工程研究院'),
    ('航空发动机研究院', '航空发动机研究院'),
    ('燃气轮机研究院', '燃气轮机研究院'),
    ('上海智能制造研究院', '上海智能制造研究院'),
    ('医疗机器人研究院', '医疗机器人研究院'),
    ('医学影像先进技术研究院', '医学影像先进技术研究院'),
    ('人工智能研究院', '人工智能研究院'),
    ('三亚崖州湾深海科技研究院', '三亚崖州湾深海科技研究院'),
    ('元知机器人研究院', '元知机器人研究院'),
    ('研究院·综合交叉', '研究院·综合交叉'),
    ('碳中和发展研究院', '碳中和发展研究院'),
    ('Bio-X研究院', 'Bio-X研究院'),
    ('Med-X研究院', 'Med-X研究院'),
    ('转化医学研究院', '转化医学研究院'),
    ('个性化医学研究院', '个性化医学研究院'),
    ('董浩云航运与物流研究院（中美物流研究院）', '董浩云航运与物流研究院（中美物流研究院）'),
    ('新农村发展研究院（农业与生物学院）', '新农村发展研究院（农业与生物学院）')
]


class Volunteer(models.Model):
    student_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    school = models.CharField(max_length=50, choices=SCHOOL_CHOICES)
    major = models.CharField(max_length=255)
    email = models.EmailField()  # 需要以@sjtu.edu.cn结尾
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)  # 加密
    application_date = models.DateField()
    labor_hours = models.IntegerField()  # >= 0
    type_preference = models.IntegerField(default=0)
    duration_preference = models.IntegerField(default=0)
    token = models.CharField(max_length=255, default='')
    token_expiration = models.DateTimeField(null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Organizer(models.Model):
    organizer_id = models.AutoField(primary_key=True)
    organizer_name = models.CharField(max_length=255)
    account = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # 加密
    application_date = models.DateField()
    token = models.CharField(max_length=255, default='')
    token_expiration = models.DateTimeField(null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    activity_name = models.CharField(max_length=255)
    activity_description = models.TextField()
    activity_tags = models.CharField(max_length=50, choices=[
        ('讲坛讲座', '讲坛讲座'),
        ('志愿公益', '志愿公益'),
        ('劳动教育', '劳动教育'),
        ('文体活动', '文体活动'),
        ('实习实践', '实习实践'),
        ('学习培训', '学习培训'),
        ('科创活动', '科创活动'),
    ])
    activity_image_path = models.CharField(max_length=255)
    application_requirements = models.TextField()
    application_start_time = models.DateTimeField() # >= 当前时间
    application_end_time = models.DateTimeField() # >= application_start_time
    activity_start_time = models.DateTimeField() # >= application_end_time
    activity_end_time = models.DateTimeField() # >= activity_start_time
    estimated_volunteer_hours = models.IntegerField()
    activity_location = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    accepted_volunteers = models.IntegerField()
    labor_hours = models.IntegerField()
    sutuo = models.CharField(max_length=255)
    notes = models.TextField()

class ActivityStatus(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE, primary_key=True)
    activity_status = models.CharField(max_length=50, choices=[
        ('未开始', '未开始'),
        ('招募中', '招募中'),
        ('已招满', '已招满'),
        ('进行中', '进行中'),
        ('已结束', '已结束'),
        ('已取消', '已取消'),
    ])
    accepted_volunteers = models.IntegerField()
    registered_volunteers = models.IntegerField()
    clicks_in_1h = models.IntegerField()
    clicks_in_12h = models.IntegerField()
    total_clicks = models.IntegerField()

class ActivityApplication(models.Model):
    application_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    application_result = models.CharField(max_length=50, choices=[
        ('待审核', '待审核'),
        ('未通过', '未通过'),
        ('已通过', '已通过'),
    ])
    application_date = models.DateTimeField()

class VolunteerActivity(models.Model):
    student = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    activity_result = models.CharField(max_length=50, choices=[
        ('已参与', '已参与'),
        ('未参与', '未参与'),
        ('参与中', '参与中'),
        ('已报名', '已报名'),
        ('已录取', '已录取'),
        ('未录取', '未录取'),
        ('已取消', '已取消'),
    ])
    class Meta:
        unique_together = (('student', 'activity'),)

class OrganizerActivity(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    activity_result = models.CharField(max_length=50, choices=[
        ('未开始', '未开始'),
        ('招募中', '招募中'),
        ('已招满', '已招满'),
        ('进行中', '进行中'),
        ('已结束', '已结束'),
        ('已取消', '已取消'),
    ])
    class Meta:
        unique_together = (('organizer', 'activity'),)

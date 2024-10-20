from django.db import models

class Volunteer(models.Model):
    student_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)  # 加密
    application_date = models.DateField()
    labor_hours = models.IntegerField()
    type_preference = models.IntegerField(default=0)
    duration_preference = models.IntegerField(default=0)

class Organizer(models.Model):
    organizer_id = models.AutoField(primary_key=True)
    organizer_name = models.CharField(max_length=255)
    account = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # 加密
    application_date = models.DateField()

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
    application_start_time = models.DateTimeField()
    application_end_time = models.DateTimeField()
    activity_start_time = models.DateTimeField()
    activity_end_time = models.DateTimeField()
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
        ('名额已满', '名额已满'),
        ('已结束', '已结束'),
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
    ])
    class Meta:
        unique_together = (('student', 'activity'),)

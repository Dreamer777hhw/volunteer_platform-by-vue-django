# Generated by Django 5.1.2 on 2024-10-20 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Activity",
            fields=[
                ("activity_id", models.AutoField(primary_key=True, serialize=False)),
                ("activity_name", models.CharField(max_length=255)),
                ("activity_description", models.TextField()),
                (
                    "activity_tags",
                    models.CharField(
                        choices=[
                            ("讲坛讲座", "讲坛讲座"),
                            ("志愿公益", "志愿公益"),
                            ("劳动教育", "劳动教育"),
                            ("文体活动", "文体活动"),
                            ("实习实践", "实习实践"),
                            ("学习培训", "学习培训"),
                            ("科创活动", "科创活动"),
                        ],
                        max_length=50,
                    ),
                ),
                ("activity_image_path", models.CharField(max_length=255)),
                ("application_requirements", models.TextField()),
                ("application_start_time", models.DateTimeField()),
                ("application_end_time", models.DateTimeField()),
                ("activity_start_time", models.DateTimeField()),
                ("activity_end_time", models.DateTimeField()),
                ("estimated_volunteer_hours", models.IntegerField()),
                ("activity_location", models.CharField(max_length=255)),
                ("contact_name", models.CharField(max_length=255)),
                ("contact_phone", models.CharField(max_length=20)),
                ("accepted_volunteers", models.IntegerField()),
                ("labor_hours", models.IntegerField()),
                ("sutuo", models.CharField(max_length=255)),
                ("notes", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Organizer",
            fields=[
                ("organizer_id", models.AutoField(primary_key=True, serialize=False)),
                ("organizer_name", models.CharField(max_length=255)),
                ("account", models.CharField(max_length=255)),
                ("password", models.CharField(max_length=255)),
                ("application_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Volunteer",
            fields=[
                (
                    "student_id",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                ("school", models.CharField(max_length=255)),
                ("major", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=255)),
                ("application_date", models.DateField()),
                ("labor_hours", models.IntegerField()),
                ("type_preference", models.IntegerField(default=0)),
                ("duration_preference", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="ActivityStatus",
            fields=[
                (
                    "activity",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="api.activity",
                    ),
                ),
                (
                    "activity_status",
                    models.CharField(
                        choices=[
                            ("未开始", "未开始"),
                            ("招募中", "招募中"),
                            ("名额已满", "名额已满"),
                            ("已结束", "已结束"),
                        ],
                        max_length=50,
                    ),
                ),
                ("accepted_volunteers", models.IntegerField()),
                ("registered_volunteers", models.IntegerField()),
                ("clicks_in_1h", models.IntegerField()),
                ("clicks_in_12h", models.IntegerField()),
                ("total_clicks", models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name="activity",
            name="organizer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.organizer"
            ),
        ),
        migrations.CreateModel(
            name="ActivityApplication",
            fields=[
                ("application_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "application_result",
                    models.CharField(
                        choices=[("待审核", "待审核"), ("未通过", "未通过"), ("已通过", "已通过")],
                        max_length=50,
                    ),
                ),
                ("application_date", models.DateTimeField()),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.activity"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.volunteer"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VolunteerActivity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "activity_result",
                    models.CharField(
                        choices=[("已参与", "已参与"), ("未参与", "未参与"), ("参与中", "参与中")],
                        max_length=50,
                    ),
                ),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.activity"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.volunteer"
                    ),
                ),
            ],
            options={
                "unique_together": {("student", "activity")},
            },
        ),
    ]

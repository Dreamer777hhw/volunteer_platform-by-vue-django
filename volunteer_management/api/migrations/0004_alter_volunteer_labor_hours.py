# Generated by Django 5.1.2 on 2024-10-24 02:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_alter_volunteer_school_organizeractivity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="volunteer",
            name="labor_hours",
            field=models.IntegerField(default=0),
        ),
    ]

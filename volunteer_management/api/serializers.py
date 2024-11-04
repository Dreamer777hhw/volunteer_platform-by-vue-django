from rest_framework import serializers
from .models import Volunteer, Organizer, Activity, ActivityStatus, ActivityApplication, VolunteerActivity, OrganizerActivity

from rest_framework import serializers
from .models import Volunteer, Organizer

class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}  # 使密码字段仅可写，不可读
        }

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}  # 使密码字段仅可写，不可读
        }

class ActivitySerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.organizer_name', read_only=True)
    registered_volunteers = serializers.IntegerField(source='activitystatus.registered_volunteers', read_only=True)
    activity_status = serializers.CharField(source='activitystatus.activity_status', read_only=True)
    volunteer_activity_result = serializers.CharField(source='volunteeractivity.activity_result', read_only=True)
    organizer_activity_result = serializers.CharField(source='organizeractivity.activity_result', read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'

class ActivityStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityStatus
        fields = '__all__'

class ActivityApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityApplication
        fields = '__all__'

class VolunteerActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerActivity
        fields = '__all__'

class OrganizerActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizerActivity
        fields = '__all__'
from rest_framework import serializers
from .models import Volunteer, Organizer, Activity, ActivityStatus, ActivityApplication, VolunteerActivity

class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
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
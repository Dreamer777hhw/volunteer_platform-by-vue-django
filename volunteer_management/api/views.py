from rest_framework import viewsets
from .models import Volunteer, Organizer, Activity, ActivityStatus, ActivityApplication, VolunteerActivity
from .serializers import VolunteerSerializer, OrganizerSerializer, ActivitySerializer, ActivityStatusSerializer, ActivityApplicationSerializer, VolunteerActivitySerializer

class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class OrganizerViewSet(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ActivityStatusViewSet(viewsets.ModelViewSet):
    queryset = ActivityStatus.objects.all()
    serializer_class = ActivityStatusSerializer

class ActivityApplicationViewSet(viewsets.ModelViewSet):
    queryset = ActivityApplication.objects.all()
    serializer_class = ActivityApplicationSerializer

class VolunteerActivityViewSet(viewsets.ModelViewSet):
    queryset = VolunteerActivity.objects.all()
    serializer_class = VolunteerActivitySerializer
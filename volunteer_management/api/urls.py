from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VolunteerViewSet, OrganizerViewSet, ActivityViewSet, ActivityStatusViewSet, ActivityApplicationViewSet, VolunteerActivityViewSet

router = DefaultRouter()
router.register(r'volunteers', VolunteerViewSet)
router.register(r'organizers', OrganizerViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'activity-status', ActivityStatusViewSet)
router.register(r'activity-applications', ActivityApplicationViewSet)
router.register(r'volunteer-activities', VolunteerActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (VolunteerViewSet, OrganizerViewSet, ActivityViewSet,
                    ActivityStatusViewSet, ActivityApplicationViewSet, VolunteerActivityViewSet,
                    LoginView, RegisterView, AccountView, AutoTokenLoginView, AutoPasswdLoginView,
                    ActivityDetailView, ActivityListView)

router = DefaultRouter()
router.register(r'volunteers', VolunteerViewSet)
router.register(r'organizers', OrganizerViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'activity-status', ActivityStatusViewSet)
router.register(r'activity-applications', ActivityApplicationViewSet)
router.register(r'volunteer-activities', VolunteerActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('account/<token>/', AccountView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('autotokenlogin/', AutoTokenLoginView.as_view(), name='autotokenlogin'),
    path('autopasswdlogin/', AutoPasswdLoginView.as_view(), name='autopasswdlogin'),
    path('activities/${activityId}/', ActivityDetailView.as_view(), name='activity-detail'),
    path('activities/', ActivityListView.as_view(), name='activity-list'),
]

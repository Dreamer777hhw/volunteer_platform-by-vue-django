from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import (VolunteerViewSet, OrganizerViewSet, ActivityViewSet,
                    ActivityStatusViewSet, ActivityApplicationViewSet, VolunteerActivityViewSet,
                    LoginView, RegisterView, AccountView, AutoTokenLoginView, AutoPasswdLoginView,
                    ActivityDetailView, ActivityListView, RecommendActivityView,
                    UserActivityView, PasswordChangeView, CreateActivityView,
                    UploadImageView, RegisterForActivityView)

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
    path('activity/<str:activity_id_hash>/', ActivityDetailView.as_view(), name='activity-detail'),
    path('activitieslist/', ActivityListView.as_view(), name='activity-list'),
    path('recommend/<str:tab>/<str:username>/', RecommendActivityView.as_view(), name='recommend-activity'),
    path('user-activities/', UserActivityView.as_view(), name='user-activity'),
    path('changepasswd/', PasswordChangeView.as_view(), name='password_change'),
    path('create_activity/', CreateActivityView.as_view(), name='create_activity'),
    path('upload/', UploadImageView.as_view(), name='upload_image'),
    path('activity/register/<str:activity_id_hash>/', RegisterForActivityView.as_view(), name='register-activity'),
]


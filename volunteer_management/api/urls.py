from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import (VolunteerViewSet, OrganizerViewSet, ActivityViewSet,
                    ActivityStatusViewSet, ActivityApplicationViewSet, VolunteerActivityViewSet,
                    LoginView, RegisterView, AccountView, AutoTokenLoginView, AutoPasswdLoginView,
                    ActivityDetailView, ActivityListView, RecommendActivityView,
                    UserActivityView, PasswordChangeView, CreateActivityView,
                    UploadImageView, RegisterForActivityView, UpdateActivityStatusView,
                    ActivityRegistrationsView, UpcomingActivitiesView, VolunteerApplicationView,
                    ApproveVolunteerApplicationView, RejectVolunteerApplicationView,
                    CancelRegistrationView, UpdateUserInfoView)

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
    path('activity/register/<str:activity_id_hash>/<str:user_id>/', RegisterForActivityView.as_view(), name='register-activity'),
    path('update-status/', UpdateActivityStatusView.as_view(), name='update-status'),
    path('activity/<str:activity_id_hash>/registrations/<str:user_id>/', ActivityRegistrationsView.as_view(), name='activity-registrations'),
    path('upcoming-activities/', UpcomingActivitiesView.as_view(), name='upcoming-activities'),
    path('applications/<int:activity_id>/', VolunteerApplicationView.as_view(), name='volunteer-applications'),
    path('applications/approve/<int:application_id>/', ApproveVolunteerApplicationView.as_view(), name='approve-volunteer-application'),
    path('applications/reject/<int:application_id>/', RejectVolunteerApplicationView.as_view(), name='reject-volunteer-application'),
    path('activity/cancel/<str:activity_id_hash>/<str:user_id>/', CancelRegistrationView.as_view()),
    path('account-update/', UpdateUserInfoView.as_view(), name='update_user_info'),
]


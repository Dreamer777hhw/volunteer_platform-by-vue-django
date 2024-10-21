from django.contrib import admin

from .models import Activity, ActivityStatus, Organizer, Volunteer, VolunteerActivity, ActivityApplication, OrganizerActivity

admin.site.register(Volunteer)
admin.site.register(Organizer)
admin.site.register(Activity)
admin.site.register(ActivityStatus)
admin.site.register(VolunteerActivity)
admin.site.register(ActivityApplication)
admin.site.register(OrganizerActivity)

# Register your models here.

from django.contrib import admin
from .models import Tutor, Session, ApptDate, Notification, Event
import nested_admin

class TutorAdmin(nested_admin.NestedModelAdmin):
    list_display = ['tutor', 'classification']
    
class SessionAdmin(admin.ModelAdmin):
    list_display = ['tutor', 'student', 'sessionID']
    list_filter = ['sessionID']
    search_fields = ['tutor', 'student', 'classID', 'notes']
    
class ApptDateAdmin(admin.ModelAdmin):
    model = ApptDate
    extra = 0

class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    extra = 0

class EventsAdmin(admin.ModelAdmin):
    model = Event
    extra = 0

admin.site.register(Tutor, TutorAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(ApptDate, ApptDateAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Event, EventsAdmin)
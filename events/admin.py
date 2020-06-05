from django.contrib import admin
from .models import Event, VideoSubmission, EventTitles

# Register your models here.
admin.site.register(Event)
admin.site.register(VideoSubmission)
admin.site.register(EventTitles)

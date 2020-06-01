from django import forms
from django.conf import settings
from .models import Event, VideoSubmission


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("name", "due_date")
        labels = {"name": "Occassion", "due_date": "Submission Deadline"}
        help_texts = {
            "due_date": "Don't forget it takes up to 48 hours to produce your video once it's published!"
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Michael's 50th Birthday"}),
            "due_date": forms.DateInput(format="%m/%d/%Y"),
        }


class EventImageForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["image"]


class VideoSubmissionForm(forms.ModelForm):
    class Meta:
        model = VideoSubmission
        fields = (
            "video",
            "uploaded_by",
        )
        labels = {"video": "Video:"}


class VideoProductionForm(forms.ModelForm):
    class Meta:
        model = VideoSubmission
        fields = ("video_thumbnail", "approved", "production_order")

from django import forms
from django.conf import settings
from .models import Event, VideoSubmission, EventTitles


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("name", "due_date")
        labels = {"name": "Occasion", "due_date": "Submission Deadline"}
        help_texts = {
            "due_date": "Don't forget it takes up to 2 business days to produce your video once it's published!"
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


class EventTitlesForm(forms.ModelForm):
    class Meta:
        model = EventTitles
        fields = ("start_title", "end_title")


class ContactSupportForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    message = forms.CharField(widget=forms.Textarea)

from django import forms
from events.models import Event


class UploadFinalVideoForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("final_video",)

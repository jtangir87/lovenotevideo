from django import forms
from events.models import Event


class UploadFinalVideoForm(forms.Form):
    final_video = forms.FileField()

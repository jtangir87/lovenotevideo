from django import forms
from events.models import Event
from bootstrap_datepicker_plus import TimePickerInput, DatePickerInput


class UploadFinalVideoForm(forms.Form):
    final_video = forms.FileField()


class AssignEditorForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("editor", "editing_due")

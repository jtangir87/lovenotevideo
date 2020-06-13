from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField(max_length=50)
    message = forms.CharField()

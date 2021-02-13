from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

REFERRAL_SOURCE = [
    ("", "----"),
    ("Friend", "Friend"),
    ("Google", "Google"),
    ("Facebook_Group", "Facebook Group"),
    ("Social_Media_Ad", "Social Media Ad"),
    ("Other", "Other"),
]


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(
        max_length=254, help_text="Required. Input a valid email address."
    )
    referral = forms.ChoiceField(
        choices=REFERRAL_SOURCE, required=False, label="How Did You Hear About Us?")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "timezone",
            "password1",
            "password2",
            "referral",
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "timezone",
            "editor",
        )

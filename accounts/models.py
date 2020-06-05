import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from timezone_field import TimeZoneField

# Create your models here.


class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    editor = models.BooleanField(default=False)
    timezone = TimeZoneField(default="US/Eastern")

    def get_absolute_url(self):
        return reverse("dashboard")

    @property
    def is_employee(self):
        return self.is_superuser or self.editor

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name="profile", on_delete=models.CASCADE
    )
    stripe_id = models.CharField(max_length=255, blank=True, null=True)

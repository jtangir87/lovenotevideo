import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    editor = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("dashboard")


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name="profile", on_delete=models.CASCADE
    )
    stripe_id = models.CharField(max_length=255, blank=True, null=True)

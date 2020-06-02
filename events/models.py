import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.dispatch import receiver
from videokit.models import VideoField, VideoSpecField

User = get_user_model()
# Create your models here.

EVENT_STATUS_CHOICES = [
    ("Open", "Open for Submissions"),
    ("Production", "Being Produced"),
    ("Delivered", "Final Product"),
    ("Complete", "Complete"),
]


def user_event_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.user.id, filename.lower())


class Event(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Event Name")
    due_date = models.DateField()
    image = models.ImageField(
        upload_to=user_event_directory_path, blank=True, null=True
    )
    status = models.CharField(max_length=255, choices=EVENT_STATUS_CHOICES)
    editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_editor",
        limit_choices_to={"editor": True},
    )

    class Meta:
        ordering = ["due_date"]

    def __str__(self):
        return self.name + " - " + self.user.last_name

    def submissions(self):
        return VideoSubmission.objects.filter(event=self.id)

    def approved_videos(self):
        return VideoSubmission.objects.filter(event=self.id, approved=True)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.event.user.id, filename.lower())


class VideoSubmission(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    video = VideoField(
        upload_to=user_directory_path,
        width_field="video_width",
        height_field="video_height",
        rotation_field="video_rotation",
        mimetype_field="video_mimetype",
        duration_field="video_duration",
        thumbnail_field="video_thumbnail",
    )
    video_width = models.IntegerField(null=True, blank=True)
    video_height = models.IntegerField(null=True, blank=True)
    video_rotation = models.FloatField(null=True, blank=True)
    video_mimetype = models.CharField(max_length=32, null=True, blank=True)
    video_duration = models.IntegerField(null=True, blank=True)
    video_thumbnail = models.ImageField(null=True, blank=True)

    video_mp4 = VideoSpecField(source="video", format="mp4")
    video_ogg = VideoSpecField(source="video", format="ogg")
    video_webm = VideoSpecField(source="video", format="webm")

    uploaded_by = models.CharField(max_length=255, verbose_name="From:")
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    production_order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["production_order", "timestamp"]

    def __str__(self):
        return self.event.name + " - " + str(self.timestamp)


@receiver(post_delete, sender=VideoSubmission)
def video_delete(sender, instance, **kwargs):
    instance.video.delete(False)
    instance.video_thumbnail.delete(False)
    instance.video_mp4.delete(False)
    instance.video_ogg.delete(False)
    instance.video_webm.delete(False)


class EventTitles(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="titles")
    start_title = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Start Title"
    )
    end_title = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="End Title"
    )

    def __str__(self):
        return self.event.name

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.dispatch import receiver
from videokit.models import VideoField, VideoSpecField
import datetime

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
    final_video = VideoField(
        upload_to=user_event_directory_path,
        thumbnail_field="final_video_thumbnail",
        blank=True,
        null=True,
    )
    final_video_mp4 = VideoSpecField(
        source="final_video", format="mp4", blank=True, null=True
    )
    final_video_thumbnail = models.ImageField(null=True, blank=True)
    delivery_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    completed_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    class Meta:
        ordering = ["due_date"]

    def __str__(self):
        return self.name + " - " + self.user.last_name

    def submissions(self):
        return VideoSubmission.objects.filter(event=self.id)

    def approved_videos(self):
        return VideoSubmission.objects.filter(event=self.id, approved=True)

    def publish(self):
        self.status = "Production"
        self.save()

    def deliver_final(self):
        self.status = "Delivered"
        self.delivery_date = datetime.datetime.now()
        self.save()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    file_name = filename.split(".")[-2]
    file_type = filename.split(".")[-1]
    return "user_{0}/{1}_{2}.{3}".format(
        instance.event.user.id, file_name.lower(), instance.id, file_type.lower()
    )


class VideoSubmission(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    video = VideoField(
        upload_to=user_directory_path, thumbnail_field="video_thumbnail",
    )
    video_thumbnail = models.ImageField(null=True, blank=True)

    video_mp4 = VideoSpecField(source="video", format="mp4")
    video_ogg = VideoSpecField(source="video", format="ogg")
    video_webm = VideoSpecField(source="video", format="webm")

    uploaded_by = models.CharField(max_length=255, verbose_name="From:")
    email = models.EmailField(blank=True, null=True)
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

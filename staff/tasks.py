from lovenotevideo.celery import app
from events.models import VideoSubmission
from celery import task


@task(name="delete_submissions")
def delete_submissions(event_id):
    subs = VideoSubmission.objects.filter(event_id=event_id)
    for sub in subs:
        sub.delete()


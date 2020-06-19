from lovenotevideo.celery import app
from events.models import Event
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.urls import reverse
from datetime import date, timedelta

from celery import task


@task(name="customer_sub_email")
def customer_sub_email(event_id, cus_email):
    event = Event.objects.filter(id=event_id).first()

    txt_template = get_template("events/emails/video_submission_customer.txt")
    html_template = get_template("events/emails/video_submission_customer.html")

    text_content = txt_template.render({"event": event})
    html_content = html_template.render({"event": event})
    from_email = "Love Note Video <support@lovenotevideo.com>"
    subject, from_email, to = (
        "Your Love Note Video Submission has been received!",
        from_email,
        cus_email,
    )
    email = EmailMultiAlternatives(subject, text_content, from_email, [to])
    email.attach_alternative(html_content, "text/html")
    email.send()


@app.task()
def upcoming_publish_day_reminder_email():
    today = date.today()
    two_days = today + timedelta(days=2)
    events = Event.objects.filter(due_date=two_days, status="Open")

    ## EMAIL USER ##
    txt_template = get_template("events/emails/upcoming_publish_day_reminder.txt")
    html_template = get_template("events/emails/upcoming_publish_day_reminder.html")

    for event in events:
        event_path = reverse("events:event_detail", kwargs={"uuid": event.uuid})
        event_url = "https://www.lovenotevideo.com{}".format(event_path)
        context = {
            "event_url": event_url,
            "event": event,
        }

        text_content = txt_template.render(context)
        html_content = html_template.render(context)
        from_email = "Love Note Video <support@lovenotevideo.com>"
        subject, from_email = (
            "It's Almost Your Submission Deadline!",
            from_email,
        )
        email = EmailMultiAlternatives(
            subject, text_content, from_email, [event.user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()


@app.task()
def publish_day_reminder_email():
    today = date.today()
    yesterday = today - timedelta(days=1)
    events = Event.objects.filter(due_date=yesterday, status="Open")

    ## EMAIL USER ##
    txt_template = get_template("events/emails/publish_day_reminder.txt")
    html_template = get_template("events/emails/publish_day_reminder.html")

    for event in events:
        event_path = reverse("events:event_detail", kwargs={"uuid": event.uuid})
        event_url = "https://www.lovenotevideo.com{}".format(event_path)
        context = {
            "event_url": event_url,
            "event": event,
        }

        text_content = txt_template.render(context)
        html_content = html_template.render(context)
        from_email = "Love Note Video <support@lovenotevideo.com>"
        subject, from_email = (
            "Hooray for Publish Day!",
            from_email,
        )
        email = EmailMultiAlternatives(
            subject, text_content, from_email, [event.user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

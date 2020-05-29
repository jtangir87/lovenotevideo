from django.shortcuts import render
from .models import Package, Addon, Order, OrderAddon
from events.models import Event, VideoSubmission
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.


def get_package(event):
    video_count = VideoSubmission.objects.filter(event=event).count()
    package = Package.objects.filter(
        min_videos__lte=video_count, max_videos__gte=video_count
    ).first()
    return package


@login_required
def publish_event(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()
    videos = VideoSubmission.objects.filter(event=event)
    package = get_package(event)
    order_total = package.price

    context = {
        "event": event,
        "videos": videos,
        "package": package,
        "order_total": order_total,
    }

    return render(request, "orders/publish_event.html", context)

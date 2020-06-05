import os
import os.path
import zipfile
from django.shortcuts import render
from django.urls import reverse
from django.template.loader import render_to_string
from lovenotevideo.mixins import (
    StaffRequiredMixin,
    EmployeeRequiredMixin,
)
from django.contrib.auth.decorators import login_required, permission_required
from django.http import (
    JsonResponse,
    HttpResponseRedirect,
    HttpResponse,
    HttpResponseForbidden,
)
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib import messages

from events.models import Event, VideoSubmission
from .forms import UploadFinalVideoForm

# Create your views here.
@login_required
@permission_required("user.is_staff", raise_exception=True)
def staff_dashboard(request):
    context = {}
    return render(request, "staff/admin_dash.html", context)


@login_required
def editor_dashboard(request):
    if request.user.is_employee:
        projects = Event.objects.filter(editor=request.user)
        open_projects = projects.filter(status="Production")
        completed_projects = projects.filter(
            Q(status="Delivered") | Q(status="Complete")
        )
        context = {
            "projects": projects,
            "open_projects": open_projects,
            "completed_projects": completed_projects,
        }

    else:
        raise PermissionDenied()
    return render(request, "staff/editor_dash.html", context)


def event_detail(request, pk):
    event = Event.objects.filter(id=pk).first()
    data = dict()
    data["html_event_detail"] = render_to_string(
        "staff/includes/partial_event_detail.html", {"event": event}, request=request
    )
    return JsonResponse(data)


@login_required
def download_files(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()
    videos = VideoSubmission.objects.filter(event=event, approved=True)

    response = HttpResponse(content_type="application/zip")
    zip_file = zipfile.ZipFile(response, "w")
    for video in videos:
        name_only = video.video.path.split(os.sep)[-1]
        production_order = str(video.production_order).zfill(3)
        ordered_name = "{}_{}".format(production_order, name_only)
        zip_file.write(video.video.path, ordered_name)
    response["Content-Disposition"] = "attachment; filename={}.zip".format(event.name)
    zip_file.close()
    return response


@login_required
def upload_final_video(request, uuid):
    if request.user.is_employee:
        event = Event.objects.filter(uuid=uuid).first()
        if request.method == "POST":
            form = UploadFinalVideoForm(
                request.POST or None, request.FILES or None, instance=event
            )
            if form.is_valid():
                event.final_video = request.FILES.get("final_video", None)
                event.deliver_final()
                event.save()
                event.final_video_mp4.generate()

                ## EMAIL CUSTOMER HERE ###
                messages.add_message(
                    request, messages.SUCCESS, "FINAL PRODUCT UPLOADED SUCCESSFULLY!"
                )
                return HttpResponseRedirect(reverse("staff:editor_dash"))
            else:
                errors = form.errors
                form = UploadFinalVideoForm(
                    request.POST or None, request.FILES or None, instance=event
                )
                context = {"form": form, "event": event}
        else:
            form = UploadFinalVideoForm(instance=event)
            context = {"form": form, "event": event}
        return render(request, "staff/upload_final.html", context)

    else:
        raise PermissionDenied()

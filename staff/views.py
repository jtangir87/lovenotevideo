import os
import os.path
import zipfile
import boto3
from django.conf import settings
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
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

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

    session = boto3.session.Session()
    client = session.client(
        "s3",
        region_name=settings.AWS_S3_REGION_NAME,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    base = getattr(settings, "BASE_DIR", "")
    temp_dir = os.path.join(base, "temp_zip_files")

    if not os.path.exists(temp_dir):
        try:
            os.makedirs(temp_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    response = HttpResponse(content_type="application/zip")
    zip_file = zipfile.ZipFile(response, "w")
    for video in videos:
        name_only = video.video.name.split(os.sep)[-1]
        temp_file_name = os.path.join(temp_dir, name_only)
        aws_file_name = "{}/{}{}".format(
            settings.AWS_LOCATION, settings.MEDIA_ROOT, video.video.name
        )
        client.download_file(
            settings.AWS_STORAGE_BUCKET_NAME, aws_file_name, temp_file_name,
        )

        production_order = str(video.production_order).zfill(3)
        ordered_name = "{}_{}".format(production_order, name_only)
        zip_file.write(temp_file_name, ordered_name)
        os.remove(temp_file_name)
    response["Content-Disposition"] = "attachment; filename={}.zip".format(event.name)
    zip_file.close()
    return response


@login_required
def upload_final_video(request, uuid):
    if request.user.is_employee:
        event = Event.objects.filter(uuid=uuid).first()
        if request.method == "POST":
            form = UploadFinalVideoForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                event.final_video = request.FILES.get("final_video", None)
                event.deliver_final()
                event.save()
                event.final_video_mp4.generate()

                ## EMAIL CUSTOMER HERE ###

                txt_template = get_template("events/emails/final_video.txt")
                html_template = get_template("events/emails/final_video.html")

                context = {
                    "video_url": request.build_absolute_uri(event.final_video.url),
                    "poster_url": request.build_absolute_uri(
                        event.final_video_thumbnail.url
                    ),
                    "event": event,
                }

                text_content = txt_template.render(context)
                html_content = html_template.render(context)
                from_email = "Love Note Video <support@lovenotevideo.com>"
                subject, from_email, to = (
                    "Your Love Note Video is Ready!",
                    from_email,
                    event.user.email,
                )
                email = EmailMultiAlternatives(subject, text_content, from_email, [to])
                email.attach_alternative(html_content, "text/html")
                email.send()

                messages.add_message(
                    request, messages.SUCCESS, "FINAL PRODUCT UPLOADED SUCCESSFULLY!"
                )
                return HttpResponseRedirect(reverse("staff:editor_dash"))
            else:
                errors = form.errors
                form = UploadFinalVideoForm(request.POST or None, request.FILES or None)
                context = {"form": form, "event": event}
        else:
            form = UploadFinalVideoForm()
            context = {"form": form, "event": event}
        return render(request, "staff/upload_final.html", context)

    else:
        raise PermissionDenied()

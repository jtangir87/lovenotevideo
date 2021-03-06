import os
import json
import datetime
from django.utils.encoding import smart_str
from django.contrib.auth import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Event, VideoSubmission, EventTitles
from .forms import (
    EventCreateForm,
    VideoSubmissionForm,
    VideoProductionForm,
    EventImageForm,
    EventTitlesForm,
    ContactSupportForm,
)
from .tasks import customer_sub_email, user_sub_email
from lovenotevideo.mixins import UserOrStaffMixin
from django.forms.models import modelformset_factory
from django.views.generic import DetailView, CreateView, TemplateView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes

import boto3

User = get_user_model()
# Create your views here.


@login_required
def event_create(request):
    user = User.objects.filter(id=request.user.id).first()
    data = dict()

    if request.method == "POST":
        form = EventCreateForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = user
            event.status = "Open"
            event.save()

            event_url = request.build_absolute_uri(
                reverse("events:event_detail", kwargs={"uuid": event.uuid})
            )

            ## EMAIL USER ##
            txt_template = get_template("events/emails/new_event.txt")
            html_template = get_template("events/emails/new_event.html")

            context = {
                "event_url": event_url,
                "event": event,
            }

            text_content = txt_template.render(context)
            html_content = html_template.render(context)
            from_email = "Love Note Video <support@lovenotevideo.com>"
            subject, from_email, to = (
                "New Love Note Created",
                from_email,
                user.email,
            )
            email = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            email.attach_alternative(html_content, "text/html")
            email.send()
            data["form_is_valid"] = True
            data["redirect_url"] = event_url
            # return HttpResponseRedirect(
            #     reverse("events:event_detail", kwargs={"uuid": event.uuid})
            # )
        else:
            errors = form.errors
            form = EventCreateForm(request.POST)
            context = {"form": form, "errors": errors}
            data["html_form"] = render_to_string(
                "events/includes/partial_event_create_form.html",
                context,
                request=request,
            )
            data["form_is_valid"] = False

    else:
        form = EventCreateForm()
        data["html_form"] = render_to_string(
            "events/includes/partial_event_create_form.html",
            {"form": form},
            request=request,
        )
    return JsonResponse(data)


@login_required
def event_update(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()
    data = dict()

    if request.method == "POST":
        form = EventCreateForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            event_url = request.build_absolute_uri(
                reverse("events:event_detail", kwargs={"uuid": event.uuid})
            )
            data["form_is_valid"] = True
            data["redirect_url"] = event_url
        else:
            errors = form.errors
            form = EventCreateForm(request.POST, instance=event)
            context = {"form": form, "errors": errors}
            data["html_form"] = render_to_string(
                "events/includes/partial_event_create_form.html",
                context,
                request=request,
            )
            data["form_is_valid"] = False

    else:
        form = EventCreateForm(instance=event)
        data["html_form"] = render_to_string(
            "events/includes/partial_event_update_form.html",
            {"form": form},
            request=request,
        )
    return JsonResponse(data)


@login_required
def event_image_upload(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()

    if request.method == "POST":
        form = EventImageForm(
            request.POST or None, request.FILES or None, instance=event
        )
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(
            reverse("events:event_detail", kwargs={"uuid": event.uuid})
        )


# class EventImageUpdate(LoginRequiredMixin, UserOrStaffMixin, UpdateView):
#     slug_url_kwarg = "uuid"
#     slug_field = "uuid"
#     model = Event
#     template_name = "events/event_detail.html"
#     success_url = reverse_lazy(
#         "events:event_detail", kwargs={"uuid": self.uuid})


class EventDetail(LoginRequiredMixin, UserOrStaffMixin, DetailView):
    slug_url_kwarg = "uuid"
    slug_field = "uuid"
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submission_url"] = reverse(
            "events:video_submission", kwargs={"uuid": self.object.uuid}
        )
        context["videos"] = VideoSubmission.objects.filter(
            event=self.object.id)
        context["image_form"] = EventImageForm()
        context["titles"] = EventTitles.objects.filter(
            event=self.object.id).first()
        return context


def video_submission(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()

    if request.method == "POST":
        form = VideoSubmissionForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            video = request.FILES.get("video", None)
            uploaded_by = request.POST.get("uploaded_by", None)
            cus_email = request.POST.get("email", None)
            sub = VideoSubmission(
                event=event, uploaded_by=uploaded_by, email=cus_email)
            sub.save()
            sub.video = video
            sub.save()

            sub.video_mp4.generate()

            ## EMAIL CUSTOMER ##
            if cus_email:
                customer_sub_email.delay(event.id, cus_email)

            ## EMAIL USER ##
            event_url = request.build_absolute_uri(
                reverse("events:event_detail", kwargs={"uuid": event.uuid})
            )

            user_sub_email.delay(event.id, sub.id, event_url)

            return HttpResponseRedirect("/thank-you")
        else:
            errors = form.errors
            form = VideoSubmissionForm(
                request.POST or None, request.FILES or None)
            context = {"form": form, "errors": errors, "event": event}
    else:
        form = VideoSubmissionForm()
        context = {"form": form, "event": event}
    return render(request, "events/video_submission.html", context)


def user_video_submission(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()

    if request.method == "POST":
        form = VideoSubmissionForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            video = request.FILES.get("video", None)
            uploaded_by = request.POST.get("uploaded_by", None)
            cus_email = request.POST.get("email", None)
            sub = VideoSubmission(
                event=event, uploaded_by=uploaded_by, email=cus_email)
            sub.save()
            sub.video = video
            sub.save()

            sub.video_mp4.generate()

            return HttpResponseRedirect(
                reverse("events:event_detail", kwargs={"uuid": event.uuid})
            )
        else:
            errors = form.errors
            form = VideoSubmissionForm(
                request.POST or None, request.FILES or None)
            context = {"form": form, "errors": errors, "event": event}
    else:
        form = VideoSubmissionForm()
        context = {"form": form, "event": event}
    return render(request, "events/user_video_submission.html", context)


class ThankYou(TemplateView):
    template_name = "events/thank_you.html"


@login_required
def event_titles(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()
    titles, created = EventTitles.objects.get_or_create(event=event)
    data = dict()

    if request.method == "POST":
        form = EventTitlesForm(request.POST, instance=titles)
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            data["html_titles"] = render_to_string(
                "events/includes/partial_event_titles.html",
                {"titles": titles, "event": event},
            )
        else:
            data["form_is_valid"] = False

    else:
        form = EventTitlesForm(instance=titles)

    context = {"form": form, "event": event}
    data["html_form"] = render_to_string(
        "events/includes/partial_event_titles_form.html", context, request=request
    )
    return JsonResponse(data)


@login_required
def production_order(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()
    ProductionOrderFormset = modelformset_factory(
        VideoSubmission, form=VideoProductionForm, extra=0, min_num=0, validate_min=True
    )
    if request.method == "POST":
        formset = ProductionOrderFormset(request.POST or None)
        if formset.is_valid():
            for form in formset:
                form.save()
        publish_url = reverse("orders:package_select", kwargs={"pk": event.pk})
        success_message = "Order and Approvals saved! <button type='button' class='btn btn-small lilac-button js-package-select' style='margin-left:10px' data-url='{}'>Click Here to Publish!</button>".format(
            publish_url
        )
        messages.add_message(
            request, messages.SUCCESS, mark_safe(success_message),
        )
        return HttpResponseRedirect(
            reverse("events:video_reorder", kwargs={"uuid": event.uuid})
        )
    else:
        formset = ProductionOrderFormset(
            queryset=VideoSubmission.objects.filter(event=event)
        )
    return render(
        request,
        "events/video_submission_reorder.html",
        {"formset": formset, "event": event},
    )


def final_video(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()
    video_url = request.build_absolute_uri(event.final_video.url)
    return render(
        request, "events/final_video.html", {
            "event": event, "video_url": video_url}
    )


@login_required
def final_video_download(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()

    path_to_file = event.final_video.path
    file_type = path_to_file.split(".")[-1]
    file_name = "Love Note Video - {0}.{1}".format(event.name, file_type)

    # session = boto3.session.Session()
    # client = session.client(
    #     "s3",
    #     region_name=settings.AWS_S3_REGION_NAME,
    #     endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    #     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    # )
    # # client.download_file(
    #     settings.AWS_STORAGE_BUCKET_NAME, aws_file_name, temp_source_file,
    # )

    chunk_size = 8192

    response = StreamingHttpResponse(FileWrapper(
        open(path_to_file, 'rb'), chunk_size), content_type="application/force-download")

    # fl = open(path_to_file, 'rb')
    # response = HttpResponse(fl, content_type="application/force-download")
    response['Content-Length'] = os.path.getsize(path_to_file)
    response["Content-Disposition"] = "attachment; filename={}".format(
        file_name)
    # response["X-Accel-Redirect"] = smart_str(path_to_file)
    return response


def contact_support(request, uuid, submitted_from):
    event = get_object_or_404(Event, uuid=uuid)
    submitted_from = submitted_from
    data = dict()

    if request.method == "POST":
        form = ContactSupportForm(request.POST or None)
        if form.is_valid():
            email = request.POST.get("email", None)
            name = request.POST.get("name", None)
            phone = request.POST.get("phone", None)
            message = request.POST.get("message", None)
            submitted_from = request.POST.get("submitted_from", None)

            txt_template = get_template("events/emails/contact_support.txt")
            html_template = get_template("events/emails/contact_support.html")

            context = {
                "event": event,
                "email": email,
                "name": name,
                "phone": phone,
                "message": message,
                "submitted_from": submitted_from,
            }

            text_content = txt_template.render(context)
            html_content = html_template.render(context)
            subject, from_email = (
                "NEW SUPPORT REQUEST",
                email,
            )
            email = EmailMultiAlternatives(
                subject, text_content, from_email, [
                    "support@lovenotevideo.com"]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False

    else:
        form = ContactSupportForm()
        data["html_form"] = render_to_string(
            "events/includes/partial_contact_support_form.html",
            {"form": form, "event": event, "submitted_from": submitted_from},
            request=request,
        )
    return JsonResponse(data)

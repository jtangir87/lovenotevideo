import os
import json
import datetime
from django.utils.encoding import smart_str
from django.contrib.auth import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Event, VideoSubmission, EventTitles
from .forms import (
    EventCreateForm,
    VideoSubmissionForm,
    VideoProductionForm,
    EventImageForm,
    EventTitlesForm,
)
from lovenotevideo.mixins import UserOrStaffMixin
from django.forms.models import modelformset_factory
from django.views.generic import DetailView, CreateView, TemplateView, View
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

            ## EMAIL USER ##
            txt_template = get_template("events/emails/new_event.txt")
            html_template = get_template("events/emails/new_event.html")

            context = {
                "event_url": request.build_absolute_uri(
                    reverse("events:event_detail", kwargs={"uuid": event.uuid})
                ),
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
            email = EmailMultiAlternatives(subject, text_content, from_email, [to])
            email.attach_alternative(html_content, "text/html")
            email.send()

            return HttpResponseRedirect(
                reverse("events:event_detail", kwargs={"uuid": event.uuid})
            )
        else:
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
            return HttpResponseRedirect(
                reverse("events:event_detail", kwargs={"uuid": event.uuid})
            )
        else:
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
        context["videos"] = VideoSubmission.objects.filter(event=self.object.id)
        context["image_form"] = EventImageForm()
        context["titles"] = EventTitles.objects.filter(event=self.object.id).first()
        return context


def video_submission(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()

    if request.method == "POST":
        form = VideoSubmissionForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            video = request.FILES.get("video", None)
            uploaded_by = request.POST.get("uploaded_by", None)
            sub = VideoSubmission(event=event, uploaded_by=uploaded_by)
            sub.save()
            sub.video = video
            sub.save()

            ## EMAIL USER ##
            txt_template = get_template("events/emails/video_submission.txt")
            html_template = get_template("events/emails/video_submission.html")

            context = {
                "event_url": request.build_absolute_uri(
                    reverse("events:event_detail", kwargs={"uuid": event.uuid})
                ),
                "event": event,
                "sub": sub,
            }

            text_content = txt_template.render(context)
            html_content = html_template.render(context)
            from_email = "Love Note Video <support@lovenotevideo.com>"
            subject, from_email, to = (
                "New Love Note Submission",
                from_email,
                event.user.email,
            )
            email = EmailMultiAlternatives(subject, text_content, from_email, [to])
            email.attach_alternative(html_content, "text/html")
            email.send()

            return HttpResponseRedirect("/thank-you")
        else:
            errors = form.errors
            form = VideoSubmissionForm(request.POST or None, request.FILES or None)
            context = {"form": form, "errors": errors, "event": event}
    else:
        form = VideoSubmissionForm()
        context = {"form": form, "event": event}
    return render(request, "events/video_submission.html", context)


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
        publish_url = reverse("orders:publish_event", kwargs={"uuid": event.uuid})
        success_message = "Order and Approvals saved! <a class='btn btn-small lilac-button' style='margin-left:10px' href='{}'>Click Here to Publish!</a>".format(
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
        request, "events/final_video.html", {"event": event, "video_url": video_url}
    )


@login_required
def final_video_download(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()
    file_name = event.final_video.path.split(os.sep)[-1]
    print(file_name)
    response = HttpResponse(content_type="application/force-download")
    response["Content-Disposition"] = "attachment; filename=%s" % (file_name)
    response["X-Sendfile"] = event.final_video.path
    return response

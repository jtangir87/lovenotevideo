import json
import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Event, VideoSubmission
from .forms import (
    EventCreateForm,
    VideoSubmissionForm,
    VideoProductionForm,
    EventImageForm,
)
from django.forms.models import modelformset_factory
from django.views.generic import DetailView, CreateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

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


class EventDetail(LoginRequiredMixin, DetailView):
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
        return context


def video_submission(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()

    if request.method == "POST":
        form = VideoSubmissionForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            video = request.FILES.get("video", None)
            uploaded_by = request.POST.get("uploaded_by", None)
            sub = VideoSubmission(event=event, video=video, uploaded_by=uploaded_by)
            sub.save()

            sub.video_mp4.generate()
            return redirect("/thank-you")
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

        return HttpResponseRedirect(
            reverse("events:video_reorder", kwargs={"uuid": event.uuid})
        )
    else:
        formset = ProductionOrderFormset(
            queryset=VideoSubmission.objects.filter(event=event)
        )
        submission_count = int(VideoSubmission.objects.filter(event=event).count()) + 1
        for form in formset:
            form.fields["production_order"].choices = [
                (x, x) for x in range(1, submission_count)
            ]
    return render(request, "events/video_submission_reorder.html", {"formset": formset})

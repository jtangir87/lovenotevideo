import datetime
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required

from events.models import Event

User = get_user_model()


class HomeView(TemplateView):
    template_name = "public/home.html"


@login_required
def dashboard(request):
    user = User.objects.filter(id=request.user.id).first()
    events = Event.objects.filter(user=user)
    context = {
        "events": events,
    }
    return render(request, "events/dashboard.html", context)


class PrivacyPolicy(TemplateView):
    template_name = "public/privacy_policy.html"


class TermsofUse(TemplateView):
    template_name = "public/terms_of_use.html"

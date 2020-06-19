import datetime
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib import messages

from .forms import ContactUsForm
from events.models import Event
from orders.models import Package

User = get_user_model()


class HomeView(TemplateView):
    template_name = "public/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["packages"] = Package.objects.filter(active=True).order_by("price")
        return context


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


def contact_us(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST or None)
        if form.is_valid():
            name = request.POST.get("name")
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            message = request.POST.get("message")

            txt_template = get_template("public/emails/contact_us.txt")
            html_template = get_template("public/emails/contact_us.html")

            context = {
                "name": name,
                "email": email,
                "subject": subject,
                "message": message,
            }

            text_content = txt_template.render(context)
            html_content = html_template.render(context)
            from_email = email
            email = EmailMultiAlternatives(
                "LNV - CONTACT US",
                text_content,
                from_email,
                ["support@lovenotevideo.com"],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.add_message(
                request, messages.SUCCESS, "Message sent successfully!",
            )
    else:
        form = ContactUsForm()

    return render(request, "public/contact_us.html", {"form": form})

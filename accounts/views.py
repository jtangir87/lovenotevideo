from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import RegisterForm, UserUpdateForm
from django.views.generic import UpdateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

CustomUser = get_user_model()

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            ## EMAIL USER ##
            txt_template = get_template("accounts/emails/registration_success.txt")
            html_template = get_template("accounts/emails/registration_success.html")

            context = {
                "dashboard_url": request.build_absolute_uri(reverse("dashboard")),
            }

            text_content = txt_template.render(context)
            html_content = html_template.render(context)
            from_email = "Love Note Video <support@lovenotevideo.com>"
            subject, from_email, to = (
                "Love Note Video Account",
                from_email,
                user.email,
            )
            email = EmailMultiAlternatives(subject, text_content, from_email, [to])
            email.attach_alternative(html_content, "text/html")
            email.send()

            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


class UserUpdate(LoginRequiredMixin, UpdateView):
    slug_url_kwarg = "uuid"
    slug_field = "uuid"
    model = CustomUser
    fields = ("first_name", "last_name", "email")
    template_name = "accounts/user_update.html"


@login_required
@permission_required("user.is_staff", raise_exception=True)
def admin_user_update(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    data = dict()
    if request.method == "POST":
        form = UserUpdateForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    else:
        form = UserUpdateForm(instance=user)
        data["html_form"] = render_to_string(
            "accounts/includes/partial_admin_user_update_form.html",
            {"form": form},
            request=request,
        )
    return JsonResponse(data)

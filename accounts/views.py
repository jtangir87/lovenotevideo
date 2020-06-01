from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm
from django.views.generic import UpdateView


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

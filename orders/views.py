import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import Package, Addon, Order, OrderAddon, Payment
from events.models import Event, VideoSubmission
from accounts.models import Profile

User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.


def get_package(event):
    video_count = VideoSubmission.objects.filter(event=event, approved=True).count()
    package = Package.objects.filter(
        min_videos__lte=video_count, max_videos__gte=video_count
    ).first()
    return package


@login_required
def publish_event(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()
    user = User.objects.filter(id=request.user.id).first()
    videos = VideoSubmission.objects.filter(event=event, approved=True)
    package = get_package(event)
    order_total = package.price
    stripe_total = int(package.price * 100)

    if request.method == "POST":
        profile, created = Profile.objects.get_or_create(user=request.user)
        print(profile.stripe_id)
        if profile.stripe_id:
            customer = profile.stripe_id
        else:
            customer = stripe.Customer.create(
                email=request.user.email,
                source=request.POST["stripeToken"],
                name=(request.user.first_name + " " + request.user.last_name),
            )
            profile.stripe_id = customer.id
            profile.save()

        charge = stripe.Charge.create(
            amount=stripe_total,
            currency="usd",
            customer=customer,
            description="Love Note Video" + " - " + event.name,
        )

        if charge.status == "succeeded":
            order = Order.objects.create(
                event=event, customer=user, package=package, order_total=order_total
            )
            Payment.objects.create(
                order=order,
                stripe_payment_id=charge.id,
                customer=user,
                event=event,
                amount=order_total,
                receipt_url=charge.receipt_url,
            )
            event.status == "Production"
            event.save()

            card = charge.payment_method_details.card

            return HttpResponseRedirect(
                reverse("orders:publish_success", kwargs={"uuid": event.uuid})
            )
    else:

        context = {
            "event": event,
            "videos": videos,
            "package": package,
            "order_total": order_total,
            "stripe_total": stripe_total,
            "key": settings.STRIPE_PUBLISHABLE_KEY,
        }

    return render(request, "orders/publish_event.html", context)


@login_required
def publish_success(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()
    return render(request, "orders/publish_successful.html", {"event": event})

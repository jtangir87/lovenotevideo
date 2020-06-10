import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from .models import Package, Addon, Order, OrderAddon, Payment, EventCoupon
from events.models import Event, VideoSubmission
from accounts.models import Profile
from django_simple_coupons.validations import validate_coupon
from django_simple_coupons.models import Coupon


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

    if videos.count() >= 1:
        package = get_package(event)
        try:
            coupon = float(event.coupon.discount_value)
        except ObjectDoesNotExist:
            coupon = 0
        order_total = package.price
        discounted_total = float(order_total) - coupon
        stripe_total = int(discounted_total * 100)

        if request.method == "POST":
            profile, created = Profile.objects.get_or_create(user=request.user)
            if discounted_total > 0:
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
                        event=event,
                        customer=user,
                        package=package,
                        order_total=discounted_total,
                    )
                    Payment.objects.create(
                        order=order,
                        stripe_payment_id=charge.id,
                        customer=user,
                        event=event,
                        amount=discounted_total,
                        receipt_url=charge.receipt_url,
                    )
                    event.publish()

                    card = charge.payment_method_details.card

            else:
                order = Order.objects.create(
                    event=event,
                    customer=user,
                    package=package,
                    order_total=discounted_total,
                )
                event.publish()

            ## EMAIL CUSTOMER HERE ###

            txt_template = get_template("orders/emails/publish_success.txt")
            html_template = get_template("orders/emails/publish_success.html")

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
                "Your Love Note Video Has Been Published!",
                from_email,
                event.user.email,
            )
            email = EmailMultiAlternatives(subject, text_content, from_email, [to])
            email.attach_alternative(html_content, "text/html")
            email.send()

            return HttpResponseRedirect(
                reverse("orders:publish_success", kwargs={"uuid": event.uuid})
            )
        else:

            context = {
                "event": event,
                "videos": videos,
                "package": package,
                "order_total": order_total,
                "discounted_total": discounted_total,
                "stripe_total": stripe_total,
                "key": settings.STRIPE_PUBLISHABLE_KEY,
            }

    else:
        messages.add_message(
            request,
            messages.WARNING,
            "Please approve and order your Love Notes before publishing",
        )
        return redirect(reverse("events:event_detail", kwargs={"uuid": event.uuid}))
    return render(request, "orders/publish_event.html", context)


class UseCouponView(View):
    def get(self, request, *args, **kwargs):
        coupon_code = request.GET.get("coupon_code")
        user = User.objects.get(id=request.user.id)

        status = validate_coupon(coupon_code=coupon_code, user=user)
        if status["valid"]:
            coupon = Coupon.objects.get(code=coupon_code)
            coupon.use_coupon(user=user)

            return HttpResponse("Discount Applied")

        return HttpResponse(status["INVALID COUPON CODE"])


@login_required
def use_coupon(request):
    event_id = request.GET.get("event_id")
    event = Event.objects.filter(id=event_id).first()
    coupon_code = request.GET.get("coupon_code")
    order_total = float(request.GET.get("order_total"))
    user = User.objects.filter(id=request.user.id).first()

    status = validate_coupon(coupon_code=coupon_code, user=user)
    if status["valid"]:
        coupon = Coupon.objects.get(code=coupon_code)
        coupon.use_coupon(user=user)

        ec, created = EventCoupon.objects.get_or_create(event=event,)
        ec.coupon = coupon
        dicount = coupon.get_discount()
        if coupon.discount.is_percentage:
            if coupon.discount.value == 100:
                discount_value = order_total
            else:
                discount_value = order_total * (coupon.discount.value / 100)
        else:
            discount_value = coupon.discount.value
        ec.discount_value = discount_value
        ec.save()

    else:
        messages.add_message(request, messages.WARNING, status["message"])

    return HttpResponseRedirect(
        reverse("orders:publish_event", kwargs={"uuid": event.uuid})
    )


@login_required
def publish_success(request, uuid):
    event = Event.objects.filter(uuid=uuid).first()
    return render(request, "orders/publish_successful.html", {"event": event})

import uuid
from django.urls import reverse
from django.db import models
from django.db.models import Sum
from events.models import Event
from django.contrib.auth import get_user_model
from django_simple_coupons.models import Coupon

User = get_user_model()

# Create your models here.
class Package(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    included_videos = models.PositiveIntegerField(
        default=10, verbose_name="Included Videos"
    )
    addtl_video_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=3,
        verbose_name="Price per Additional Video",
    )
    min_videos = models.PositiveIntegerField(blank=True, null=True)
    max_videos = models.PositiveIntegerField(blank=True, null=True)
    sample_video_url = models.URLField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return self.name + " - " + str(self.price)

    def get_status(self):
        if self.active:
            return "Active"
        else:
            return "Inactive"

    def get_absolute_url(self):
        return reverse("orders:package_list")


class Addon(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return self.name + " - " + str(self.price)


class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        User, related_name="published_orders", on_delete=models.CASCADE
    )
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    order_total = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            self.customer.last_name
            + " - "
            + self.event.name
            + " - "
            + str(self.created_at)
        )

    def get_payments(self):
        return Payment.objects.filter(order=self.id)

    def payments_sum(self):
        total_payments = Payment.objects.filter(order=self.id).aggregate(Sum("amount"))
        return total_payments["amount__sum"]


class OrderAddon(models.Model):
    order = models.ForeignKey(Order, related_name="add_ons", on_delete=models.CASCADE)
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return "%s - %s" % self.order.id, self.addon.name


class Payment(models.Model):
    order = models.ForeignKey(Order, related_name="payments", on_delete=models.CASCADE)
    stripe_payment_id = models.CharField(max_length=100)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, related_name="event_payments", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    receipt_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event.name + " - " + str(self.id)


class EventCoupon(models.Model):
    event = models.OneToOneField(Event, related_name="coupon", on_delete=models.CASCADE)
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, blank=True, null=True
    )
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, null=True)
    discount_value = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return self.event.name

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required, permission_required

from lovenotevideo.mixins import StaffRequiredMixin
from .models import (
    Coupon,
    CouponUser,
    Discount,
    Ruleset,
    AllowedUsersRule,
    MaxUsesRule,
    ValidityRule,
)

# Create your views here.
class CouponList(StaffRequiredMixin, ListView):
    model = Coupon
    context_object_name = "coupons"
    template_name = "coupons/coupon_list.html"


class CouponUserList(StaffRequiredMixin, ListView):
    model = CouponUser
    context_object_name = "coupons"
    template_name = "coupons/coupon_user_list.html"


@login_required
@permission_required("user.is_staff", raise_exception=True)
def discounts_rulesets_list(request):
    discounts = Discount.objects.all()
    rulesets = Ruleset.objects.all()
    allowed_users = AllowedUsersRule.objects.all()
    max_uses = MaxUsesRule.objects.all()
    validity_rules = ValidityRule.objects.all()

    context = {
        "discounts": discounts,
        "rulesets": rulesets,
        "allowed_users": allowed_users,
        "max_uses": max_uses,
        "validity_rules": validity_rules,
    }

    return render(request, "coupons/discounts_rulesets_list.html", context)


class CouponCreateView(StaffRequiredMixin, CreateView):
    model = Coupon
    fields = ("code", "discount", "ruleset")
    template_name = "coupons/coupon_create_form.html"

    def get_success_url(self):
        return reverse("coupons:coupon_list")

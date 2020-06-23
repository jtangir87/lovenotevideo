from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import render_to_string
from django.http import JsonResponse

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
from .forms import (
    RulesetForm,
    DiscountForm,
    AllowedUsersForm,
    MaxUsesForm,
    ValidityForm,
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


def save_ruleset_form(request, form, template_name):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
        else:
            data["form_is_valid"] = False
    context = {"form": form}
    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@login_required
@permission_required("user.is_staff", raise_exception=True)
def ruleset_create(request):
    if request.method == "POST":
        form = RulesetForm(request.POST)
    else:
        form = RulesetForm()
    return save_ruleset_form(
        request, form, "coupons/includes/partial_ruleset_create_form.html"
    )


@login_required
@permission_required("user.is_staff", raise_exception=True)
def ruleset_update(request, pk):
    ruleset = Ruleset.objects.filter(id=pk).first()
    if request.method == "POST":
        form = RulesetForm(request.POST, instance=ruleset)
    else:
        form = RulesetForm(instance=ruleset)
    return save_ruleset_form(
        request, form, "coupons/includes/partial_ruleset_update_form.html"
    )


@login_required
@permission_required("user.is_staff", raise_exception=True)
def discount_create(request):
    if request.method == "POST":
        form = DiscountForm(request.POST)
    else:
        form = DiscountForm()
    return save_ruleset_form(
        request, form, "coupons/includes/partial_discount_create_form.html"
    )


@login_required
@permission_required("user.is_staff", raise_exception=True)
def discount_update(request, pk):
    discount = Discount.objects.filter(id=pk).first()
    if request.method == "POST":
        form = DiscountForm(request.POST, instance=discount)
    else:
        form = DiscountForm(instance=discount)
    return save_ruleset_form(
        request, form, "coupons/includes/partial_discount_update_form.html"
    )

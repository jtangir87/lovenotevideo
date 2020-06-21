from django.shortcuts import render
from django.views.generic import ListView

from lovenotevideo.mixins import StaffRequiredMixin
from .models import Coupon, CouponUser

# Create your views here.
class CouponList(StaffRequiredMixin, ListView):
    model = Coupon
    context_object_name = "coupons"
    template_name = "coupons/coupon_list.html"


class CouponUserList(StaffRequiredMixin, ListView):
    model = CouponUser
    context_object_name = "coupons"
    template_name = "coupons/coupon_user_list.html"

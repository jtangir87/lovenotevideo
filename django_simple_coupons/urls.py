"""Coupons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import CouponList, CouponUserList, discounts_rulesets_list, CouponCreateView

app_name = "coupons"

urlpatterns = [
    path("coupons/list", CouponList.as_view(), name="coupon_list"),
    path("coupons/list-by-user", CouponUserList.as_view(), name="coupon_user_list"),
    path(
        "coupons/discount-ruleset-list",
        discounts_rulesets_list,
        name="discounts_rulesets_list",
    ),
    path("coupons/create", CouponCreateView.as_view(), name="coupon_create"),
]

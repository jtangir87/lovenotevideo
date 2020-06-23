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
from .views import (
    CouponList,
    CouponUserList,
    discounts_rulesets_list,
    CouponCreateView,
    ruleset_create,
    ruleset_update,
    discount_create,
    discount_update,
)

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
    ## DISCOUNTS AND RULESETS AJAX PATHS ##
    path("coupons/ruleset/create", ruleset_create, name="ruleset_create"),
    path("coupons/ruleset/<int:pk>/update", ruleset_update, name="ruleset_update"),
    path("coupons/discount/create", discount_create, name="discount_create"),
    path("coupons/discount/<int:pk>/update", discount_update, name="discount_update"),
]

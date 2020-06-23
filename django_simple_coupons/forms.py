from django import forms
from .models import (
    Coupon,
    CouponUser,
    Discount,
    Ruleset,
    AllowedUsersRule,
    MaxUsesRule,
    ValidityRule,
)


class RulesetForm(forms.ModelForm):
    class Meta:
        model = Ruleset
        fields = ("allowed_users", "max_uses", "validity")


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ("value", "is_percentage")


class AllowedUsersForm(forms.ModelForm):
    class Meta:
        model = AllowedUsersRule
        fields = ("users", "all_users")


class MaxUsesForm(forms.ModelForm):
    class Meta:
        model = MaxUsesRule
        fields = ("max_uses", "is_infinite", "uses_per_user")


class ValidityForm(forms.ModelForm):
    class Meta:
        model = ValidityRule
        fields = ("expiration_date", "is_active")

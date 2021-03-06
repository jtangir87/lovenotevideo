"""lovenotevideo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomeView,
    dashboard,
    PrivacyPolicy,
    TermsofUse,
    contact_us,
    package_sample,
    FAQ,
)

urlpatterns = [
    path("dev/backend", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("events.urls")),
    path("", include("orders.urls")),
    path("", include("staff.urls")),
    path("", include("django_simple_coupons.urls")),
    path("", include("django.contrib.auth.urls")),
    path("", HomeView.as_view(), name="home"),
    path("privacy-policy", PrivacyPolicy.as_view(), name="privacy_policy"),
    path("terms-of-use", TermsofUse.as_view(), name="terms_of_use"),
    path("dashboard", dashboard, name="dashboard"),
    path("contact", contact_us, name="contact_us"),
    path("faq", FAQ.as_view(), name="faq"),
    path("package/<int:pk>/sample", package_sample, name="package_sample"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

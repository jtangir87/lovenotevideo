"""events URL Configuration

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
    EventDetail,
    event_create,
    video_submission,
    ThankYou,
    production_order,
    event_image_upload,
)

app_name = "events"

urlpatterns = [
    path("create", event_create, name="event_create"),
    path("<uuid:uuid>", EventDetail.as_view(), name="event_detail"),
    path("<uuid:uuid>/submission", video_submission, name="video_submission"),
    path("thank-you", ThankYou.as_view(), name="thank_you"),
    path("<uuid:uuid>/reorder", production_order, name="video_reorder"),
    path("<uuid:uuid>/image", event_image_upload, name="event_image_upload"),
]

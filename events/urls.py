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
    event_update,
    video_submission,
    ThankYou,
    production_order,
    event_image_upload,
    event_titles,
    final_video,
    final_video_download,
)

app_name = "events"

urlpatterns = [
    path("create", event_create, name="event_create"),
    path("<uuid:uuid>", final_video, name="final_video"),
    path("<uuid:uuid>/download", final_video_download, name="final_video_download"),
    path("dashboard/<uuid:uuid>/update", event_update, name="event_update"),
    path("dashboard/<uuid:uuid>", EventDetail.as_view(), name="event_detail"),
    path("dashboard/<uuid:uuid>/titles", event_titles, name="set_titles"),
    path("<uuid:uuid>/submission", video_submission, name="video_submission"),
    path("thank-you", ThankYou.as_view(), name="thank_you"),
    path("dashboard/<uuid:uuid>/reorder", production_order, name="video_reorder"),
    path("dashboard/<uuid:uuid>/image", event_image_upload, name="event_image_upload"),
]

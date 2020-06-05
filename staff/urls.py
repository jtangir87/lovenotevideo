"""staff URL Configuration

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
    staff_dashboard,
    editor_dashboard,
    event_detail,
    upload_final_video,
    download_files,
)

app_name = "staff"

urlpatterns = [
    path("staff/dashboard", staff_dashboard, name="staff_dash"),
    path("editor/dashboard", editor_dashboard, name="editor_dash"),
    path("editor/event/<int:pk>/details", event_detail, name="event_detail"),
    path(
        "editor/event/<uuid:uuid>/upload-final",
        upload_final_video,
        name="upload_final_video",
    ),
    path("editor/event/<uuid:uuid>/download", download_files, name="download_files"),
]

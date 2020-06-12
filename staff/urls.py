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
    assign_editor,
    UserList,
    EditorList,
    OpenEventsList,
    PublishedEventsList,
    ExpiredEventsList,
)

app_name = "staff"

urlpatterns = [
    path("staff/dashboard", staff_dashboard, name="staff_dash"),
    path("staff/event/<int:pk>/assign-editor", assign_editor, name="assign_editor"),
    path("staff/user-list", UserList.as_view(), name="user_list"),
    path("staff/editor-list", EditorList.as_view(), name="editor_list"),
    path("staff/events/open", OpenEventsList.as_view(), name="open_events"),
    path(
        "staff/events/published", PublishedEventsList.as_view(), name="published_events"
    ),
    path("staff/events/expired", ExpiredEventsList.as_view(), name="expired_events"),
    path("editor/dashboard", editor_dashboard, name="editor_dash"),
    path("editor/event/<int:pk>/details", event_detail, name="event_detail"),
    path(
        "editor/event/<uuid:uuid>/upload-final",
        upload_final_video,
        name="upload_final_video",
    ),
    path("editor/event/<uuid:uuid>/download", download_files, name="download_files"),
]

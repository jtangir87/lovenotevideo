"""orders URL Configuration

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
from .views import publish_event, publish_success, use_coupon

app_name = "orders"

urlpatterns = [
    path("<uuid:uuid>/publish", publish_event, name="publish_event"),
    path("<uuid:uuid>/publish/success", publish_success, name="publish_success"),
    path("<uuid:uuid>/publish/success", publish_success, name="publish_success"),
    path("orders/coupon", use_coupon, name="use_coupon"),
]

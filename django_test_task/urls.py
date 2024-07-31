from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        include("simple_app.urls", namespace="simple_app"),
    ),
]

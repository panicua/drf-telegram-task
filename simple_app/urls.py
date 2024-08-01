from django.urls import path, include
from rest_framework import routers

from simple_app import views

app_name = "simple_app"

router = routers.DefaultRouter()
router.register("books", views.BookViewSet, basename="books")

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", include(router.urls)),
]

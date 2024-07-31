from django.urls import path, include
from rest_framework import routers

from . import views


app_name = "simple_app"

router = routers.DefaultRouter()
router.register("", views.BookViewSet, basename="books")

urlpatterns = [
    path("", views.index, name="index"),
    path("api/books/", include(router.urls)),
]

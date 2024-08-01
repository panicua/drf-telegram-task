from decouple import config
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin

from simple_app.models import Book
from simple_app.serializers import BookSerializer


def index(request):
    return render(
        request,
        "simple_app/index.html",
        {"host_base_url": config("HOST_BASE_URL")},
    )


class BookViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

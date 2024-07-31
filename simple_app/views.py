from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin

from simple_app.models import Book
from simple_app.serializers import BookSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class BookViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

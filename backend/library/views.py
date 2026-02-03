from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .filters import AuthorFilter, BookFilter, BorrowRecordFilter, CategoryFilter
from .models import Author, Book, BorrowRecord, Category
from .paginations import DefaultPagination
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    BorrowRecordSerializer,
    CategorySerializer,
    UserSerializer,
)

User = get_user_model()


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter
    pagination_class = DefaultPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    pagination_class = DefaultPagination


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("category").prefetch_related("author")
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    pagination_class = DefaultPagination


class BorrowRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BorrowRecordFilter
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = BorrowRecord.objects.select_related("book", "user")

        book_pk = self.kwargs.get("book_pk")
        if book_pk:
            queryset = queryset.filter(book_id=book_pk)

        user_pk = self.kwargs.get("user_pk")
        if user_pk:
            queryset = queryset.filter(user_id=user_pk)

        return queryset


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    pagination_class = DefaultPagination
    queryset = User.objects.only("id")

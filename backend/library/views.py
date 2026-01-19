from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .filters import (
    AuthorFilter,
    BookFilter,
    BorrowRecordFilter,
    CategoryFilter,
    MemberFilter,
)
from .models import Author, Book, BorrowRecord, Category, Member
from .paginations import DefaultPagination
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    BorrowRecordSerializer,
    CategorySerializer,
    MemberSerializer,
)


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


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MemberFilter
    pagination_class = DefaultPagination


class BorrowRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BorrowRecordFilter
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = BorrowRecord.objects.select_related("book", "member")

        book_pk = self.kwargs.get("book_pk")
        if book_pk:
            queryset = queryset.filter(book_id=book_pk)

        member_pk = self.kwargs.get("member_pk")
        if member_pk:
            queryset = queryset.filter(member_id=member_pk)

        return queryset

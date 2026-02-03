from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.permissions import DjangoModelPermissions
from drf_yasg.utils import swagger_auto_schema

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
    """Manage authors (list, retrieve, create, update, delete)."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter
    pagination_class = DefaultPagination
    permission_classes = [DjangoModelPermissions]

    @swagger_auto_schema(operation_summary="List authors")
    def list(self, request, *args, **kwargs):
        """Retrieve all authors."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve an author")
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single author by ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create an author",
        operation_description="Only users with author add permission can create.",
        request_body=AuthorSerializer,
        responses={201: AuthorSerializer, 400: "Bad Request"},
    )
    def create(self, request, *args, **kwargs):
        """Create a new author."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update an author",
        operation_description="Only users with author change permission can update.",
        request_body=AuthorSerializer,
        responses={200: AuthorSerializer, 400: "Bad Request"},
    )
    def update(self, request, *args, **kwargs):
        """Update an author."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update an author",
        operation_description="Only users with author change permission can update.",
        request_body=AuthorSerializer,
        responses={200: AuthorSerializer, 400: "Bad Request"},
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update an author."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete an author",
        operation_description="Only users with author delete permission can delete.",
        responses={204: "No Content"},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete an author."""
        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    """Manage categories (list, retrieve, create, update, delete)."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    pagination_class = DefaultPagination
    permission_classes = [DjangoModelPermissions]

    @swagger_auto_schema(operation_summary="List categories")
    def list(self, request, *args, **kwargs):
        """Retrieve all categories."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve a category")
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single category by ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a category",
        operation_description="Only users with category add permission can create.",
        request_body=CategorySerializer,
        responses={201: CategorySerializer, 400: "Bad Request"},
    )
    def create(self, request, *args, **kwargs):
        """Create a new category."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a category",
        operation_description="Only users with category change permission can update.",
        request_body=CategorySerializer,
        responses={200: CategorySerializer, 400: "Bad Request"},
    )
    def update(self, request, *args, **kwargs):
        """Update a category."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a category",
        operation_description="Only users with category change permission can update.",
        request_body=CategorySerializer,
        responses={200: CategorySerializer, 400: "Bad Request"},
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update a category."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a category",
        operation_description="Only users with category delete permission can delete.",
        responses={204: "No Content"},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a category."""
        return super().destroy(request, *args, **kwargs)


class BookViewSet(viewsets.ModelViewSet):
    """Manage books (public list/retrieve; create/update/delete for permitted users)."""

    queryset = Book.objects.select_related("category").prefetch_related("author")
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    pagination_class = DefaultPagination

    def get_permissions(self):
        if self.action in {"list", "retrieve"}:
            permission_classes = [AllowAny]
        else:
            permission_classes = [DjangoModelPermissions]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(operation_summary="List books")
    def list(self, request, *args, **kwargs):
        """Retrieve all books."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve a book")
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single book by ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a book by librarian",
        operation_description="Only users with book add permission can create.",
        request_body=BookSerializer,
        responses={201: BookSerializer, 400: "Bad Request"},
    )
    def create(self, request, *args, **kwargs):
        """Create a new book."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a book",
        operation_description="Only users with book change permission can update.",
        request_body=BookSerializer,
        responses={200: BookSerializer, 400: "Bad Request"},
    )
    def update(self, request, *args, **kwargs):
        """Update a book."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a book",
        operation_description="Only users with book change permission can update.",
        request_body=BookSerializer,
        responses={200: BookSerializer, 400: "Bad Request"},
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update a book."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a book",
        operation_description="Only users with book delete permission can delete.",
        responses={204: "No Content"},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a book."""
        return super().destroy(request, *args, **kwargs)


class BorrowRecordViewSet(viewsets.ModelViewSet):
    """Manage borrow records (list, retrieve, create, update, delete).

    Supports nested routes by book and by user for filtered access.
    """

    serializer_class = BorrowRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BorrowRecordFilter
    pagination_class = DefaultPagination
    permission_classes = [DjangoModelPermissions]

    @swagger_auto_schema(operation_summary="List borrow records")
    def list(self, request, *args, **kwargs):
        """Retrieve all borrow records."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve a borrow record")
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single borrow record by ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a borrow record",
        operation_description="Only users with borrow record add permission can create.",
        request_body=BorrowRecordSerializer,
        responses={201: BorrowRecordSerializer, 400: "Bad Request"},
    )
    def create(self, request, *args, **kwargs):
        """Create a new borrow record."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a borrow record",
        operation_description="Only users with borrow record change permission can update.",
        request_body=BorrowRecordSerializer,
        responses={200: BorrowRecordSerializer, 400: "Bad Request"},
    )
    def update(self, request, *args, **kwargs):
        """Update a borrow record."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a borrow record",
        operation_description="Only users with borrow record change permission can update.",
        request_body=BorrowRecordSerializer,
        responses={200: BorrowRecordSerializer, 400: "Bad Request"},
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update a borrow record."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a borrow record",
        operation_description="Only users with borrow record delete permission can delete.",
        responses={204: "No Content"},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a borrow record."""
        return super().destroy(request, *args, **kwargs)

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
    """Read-only access to users for administrative views."""
    serializer_class = UserSerializer
    pagination_class = DefaultPagination
    queryset = User.objects.only("id")
    permission_classes = [DjangoModelPermissions]

    @swagger_auto_schema(operation_summary="List users")
    def list(self, request, *args, **kwargs):
        """Retrieve all users."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve a user")
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single user by ID."""
        return super().retrieve(request, *args, **kwargs)

from django_filters import rest_framework as filters

from .models import Author, Book, BorrowRecord, Category


class AuthorFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Author
        fields = ["name"]


class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Category
        fields = ["name"]


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    isbn = filters.CharFilter(field_name="isbn", lookup_expr="exact")
    category_id = filters.UUIDFilter(field_name="category_id")
    author_id = filters.UUIDFilter(field_name="author__id")

    class Meta:
        model = Book
        fields = ["title", "isbn", "category_id", "author_id"]


class BorrowRecordFilter(filters.FilterSet):
    status = filters.CharFilter(field_name="status", lookup_expr="exact")
    user_id = filters.UUIDFilter(field_name="user_id")
    book_id = filters.UUIDFilter(field_name="book_id")
    due_date = filters.DateFromToRangeFilter(field_name="due_date")

    class Meta:
        model = BorrowRecord
        fields = ["status", "user_id", "book_id", "due_date"]

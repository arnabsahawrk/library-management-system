from uuid import uuid4
from django.db import models


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    author = models.ManyToManyField(Author, related_name="books")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="books"
    )
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class BorrowRecord(models.Model):
    Active, Returned, Overdue = "A", "R", "O"
    Options = [(Active, "Active"), (Returned, "R"), (Overdue, "O")]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="member")
    borrow_date = models.DateTimeField()
    due_date = models.DateField()
    return_date = models.DateTimeField()
    status = models.CharField(max_length=1, choices=Options, default=Active)

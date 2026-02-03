from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    author = models.ManyToManyField(Author, related_name="books")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="books"
    )
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BorrowRecord(models.Model):
    ACTIVE = "Active"
    RETURNED = "Returned"
    OVERDUE = "Overdue"

    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (RETURNED, "Returned"),
        (OVERDUE, "Overdue"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    book = models.ForeignKey(
        Book, on_delete=models.PROTECT, related_name="borrow_records"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrow_records"
    )
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)

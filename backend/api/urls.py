from django.urls import include, path

from rest_framework.routers import DefaultRouter

from rest_framework_nested import routers

from library import views


router = DefaultRouter()
router.register("authors", views.AuthorViewSet, basename="author")
router.register("categories", views.CategoryViewSet, basename="category")
router.register("books", views.BookViewSet, basename="book")
router.register("members", views.MemberViewSet, basename="member")
router.register("borrow-records", views.BorrowRecordViewSet, basename="borrow-record")

books_router = routers.NestedDefaultRouter(router, "books", lookup="book")
books_router.register(
    "borrow-records", views.BorrowRecordViewSet, basename="book-borrow-record"
)

members_router = routers.NestedDefaultRouter(router, "members", lookup="member")
members_router.register(
    "borrow-records", views.BorrowRecordViewSet, basename="member-borrow-record"
)


urlpatterns = [
    path("", include(router.urls)),
    path("", include(books_router.urls)),
    path("", include(members_router.urls)),
]

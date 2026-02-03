from django.urls import include, path

from rest_framework.routers import DefaultRouter

from rest_framework_nested import routers

from library import views


router = DefaultRouter()
router.register("authors", views.AuthorViewSet, basename="author")
router.register("categories", views.CategoryViewSet, basename="category")
router.register("books", views.BookViewSet, basename="book")
router.register("users", views.UserViewSet, basename="user")


books_router = routers.NestedDefaultRouter(router, "books", lookup="book")
books_router.register(
    "borrow-records", views.BorrowRecordViewSet, basename="book-borrow-record"
)

users_router = routers.NestedDefaultRouter(router, "users", lookup="user")
users_router.register(
    "borrow-records", views.BorrowRecordViewSet, basename="user-borrow-record"
)


urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("", include(router.urls)),
    path("", include(books_router.urls)),
    path("", include(users_router.urls)),
]

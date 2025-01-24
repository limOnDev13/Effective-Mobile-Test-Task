"""Module with urlpatterns."""

from django.urls import path

from .views import (
    OrderCreateView,
    OrderDeleteView,
    OrderDetailView,
    OrderListView,
    OrderUpdateView,
)

app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="orders-list"),
    path("new/", OrderCreateView.as_view(), name="orders-create"),
    path("<int:pk>/", OrderDetailView.as_view(), name="orders-detail"),
    path("<int:pk>/update/", OrderUpdateView.as_view(), name="orders-update"),
    path("<int:pk>/delete/", OrderDeleteView.as_view(), name="orders-delete"),
]

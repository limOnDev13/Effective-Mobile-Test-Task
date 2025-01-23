"""Module with urlpatterns."""

from django.urls import path

from .views import OrderListView, OrderCreateView

app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="orders-list"),
    path("new/", OrderCreateView.as_view(), name="orders-create"),
]

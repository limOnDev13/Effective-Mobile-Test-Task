"""Module with urlpatterns."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api, views

app_name = "orders"

routers = DefaultRouter()
routers.register("", api.OrderViewSet)

urlpatterns = [
    path("", views.OrderListView.as_view(), name="orders-list"),
    path("revenue/", views.get_revenue_per_shift, name="orders-revenue"),
    path("new/", views.OrderCreateView.as_view(), name="orders-create"),
    path("<int:pk>/", views.OrderDetailView.as_view(), name="orders-detail"),
    path("<int:pk>/update/", views.OrderUpdateView.as_view(), name="orders-update"),
    path("<int:pk>/delete/", views.OrderDeleteView.as_view(), name="orders-delete"),
    path("api/", include(routers.urls)),
]

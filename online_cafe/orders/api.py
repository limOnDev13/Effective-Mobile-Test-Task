"""Module with api views."""

from rest_framework.viewsets import ModelViewSet

from .models import Order
from .serializers import CreateOrderSerializer, OrderSerializer, UpdateOrderSerializer


class OrderViewSet(ModelViewSet):
    """Order api ModelViewSet."""

    queryset = Order.objects.prefetch_related("items").all()

    def get_serializer_class(self):
        """Return serializer depends on action."""
        if self.action == "create":
            return CreateOrderSerializer
        elif self.action == "update" or self.action == "partial_update":
            return UpdateOrderSerializer
        else:
            return OrderSerializer

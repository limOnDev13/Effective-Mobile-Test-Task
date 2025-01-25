"""Module with DRF serializers."""

from rest_framework import serializers

from .models import Order


class CreateOrderSerializer(serializers.ModelSerializer):
    """Serializer for creating a new order."""

    class Meta:
        """Meta class."""

        model = Order
        fields = (
            "table_number",
            "items",
        )


class UpdateOrderSerializer(serializers.ModelSerializer):
    """Serializer for updating the order."""

    class Meta:
        """Meta class."""

        model = Order
        fields = (
            "status",
            "items",
        )


class OrderSerializer(serializers.ModelSerializer):
    """Base order serializer."""

    class Meta:
        """Meta class."""

        model = Order
        fields = ("pk", "table_number", "items", "status", "total_price")

"""Module with tests."""

from django.test import TestCase
from django.urls import reverse
from .models import Order


class OrderListViewTest(TestCase):
    """Test case class for testing OrderListView."""

    fixtures = [
        "../fixtures/dishes-fixture.json",
        "../fixtures/orders-fixture.json",
    ]

    def test_orders(self):
        """Test getting list of orders."""
        response = self.client.get(reverse("orders:orders-list"))

        self.assertQuerySetEqual(
            qs=Order.objects.order_by("pk").all(),
            values=sorted((s.pk for s in response.context["orders"])),
            transform=lambda p: p.pk,
        )

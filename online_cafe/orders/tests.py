"""Module with tests."""

import random
from typing import List

from django.test import TestCase
from django.urls import reverse
from menu.factories import DishFactory
from menu.models import Dish

from .factories import OrderFactory
from .models import Order


class OrderListViewTest(TestCase):
    """Test case class for testing OrderListView."""

    fixtures = [
        "../fixtures/dishes-fixture.json",
        "../fixtures/orders-fixture.json",
    ]

    def test_get_all_orders(self):
        """Test getting list of orders."""
        response = self.client.get(reverse("orders:orders-list"))

        self.assertQuerySetEqual(
            qs=Order.objects.order_by("pk").all(),
            values=sorted((s.pk for s in response.context["orders"])),
            transform=lambda p: p.pk,
        )

    def test_get_order_with_get_param_table_number(self):
        """Test getting orders with table_number from GET params."""
        table_nums: List[int] = random.choices(
            Order.objects.values_list("table_number", flat=True).all(), k=10
        )
        base_url: str = reverse("orders:orders-list")

        for table_number in table_nums:
            url_with_get_params: str = "?".join(
                (base_url, f"table_number={table_number}")
            )
            response = self.client.get(url_with_get_params)

            self.assertQuerySetEqual(
                qs=Order.objects.filter(table_number=table_number).order_by("pk").all(),
                values=sorted((s.pk for s in response.context["orders"])),
                transform=lambda p: p.pk,
            )


class OrderDetailViewTest(TestCase):
    """Test case class for testing OrderDetailView."""

    def setUp(self):
        self.dishes: List[Dish] = [
            DishFactory.create() for _ in range(random.randint(1, 10))
        ]
        self.order = OrderFactory.create(items=self.dishes)

    def tearDown(self):
        self.order.delete()
        for dish in self.dishes:
            dish.delete()

    def test_get_order(self):
        """Test getting details about order."""
        response = self.client.get(
            reverse("orders:orders-detail", kwargs={"pk": self.order.pk})
        )

        self.assertEqual(response.status_code, 200)

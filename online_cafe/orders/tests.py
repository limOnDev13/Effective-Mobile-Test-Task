"""Module with tests."""

import random
from typing import List

from django.db.models import Q
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

    def test_get_orders_with_get_param_table_number(self):
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

    def test_get_orders_with_get_param_status(self):
        """Test getting orders with status from GET params."""
        for i in range(1, 4):
            statuses_params: List[str] = random.choices(
                list(Order.STATUSES.values()), k=random.randint(1, i)
            )
            base_url: str = reverse("orders:orders-list")

            url_with_get_params: str = "?".join(
                (base_url, "&".join((f"status={status}" for status in statuses_params)))
            )
            response = self.client.get(url_with_get_params)

            statuses_filter = Q(status=statuses_params[0])
            for j in range(1, len(statuses_params)):
                statuses_filter = statuses_filter | Q(status=statuses_params[j])

            self.assertQuerySetEqual(
                qs=Order.objects.filter(statuses_filter).order_by("pk").all(),
                values=sorted((s.pk for s in response.context["orders"])),
                transform=lambda p: p.pk,
            )

    def test_get_orders_with_get_param(self):
        """Test getting orders with GET params."""
        for i in range(1, 4):
            table_nums: List[int] = random.choices(
                Order.objects.values_list("table_number", flat=True).all(), k=10
            )
            statuses_params: List[str] = random.choices(
                list(Order.STATUSES.values()), k=random.randint(1, i)
            )

            base_url: str = reverse("orders:orders-list")
            for table_number in table_nums:
                url_with_get_params: str = "?".join(
                    (
                        base_url,
                        "&".join(
                            (
                                f"table_number={table_number}",
                                *(f"status={status}" for status in statuses_params),
                            )
                        ),
                    )
                )
                response = self.client.get(url_with_get_params)

                statuses_filter = Q(status=statuses_params[0])
                for j in range(1, len(statuses_params)):
                    statuses_filter = statuses_filter | Q(status=statuses_params[j])
                statuses_filter = statuses_filter & Q(table_number=table_number)

                self.assertQuerySetEqual(
                    qs=Order.objects.filter(statuses_filter).order_by("pk").all(),
                    values=sorted((s.pk for s in response.context["orders"])),
                    transform=lambda p: p.pk,
                )


class OrderDetailViewTest(TestCase):
    """Test case class for testing OrderDetailView."""

    def setUp(self):
        """Set up."""
        self.dishes: List[Dish] = [
            DishFactory.create() for _ in range(random.randint(1, 10))
        ]
        self.order = OrderFactory.create(items=self.dishes)

    def tearDown(self):
        """Tear down."""
        self.order.delete()
        for dish in self.dishes:
            dish.delete()

    def test_get_order(self):
        """Test getting details about order."""
        response = self.client.get(
            reverse("orders:orders-detail", kwargs={"pk": self.order.pk})
        )

        self.assertEqual(response.status_code, 200)


class OrderCreateViewTest(TestCase):
    """Test case class for testing OrderCreateView."""

    def setUp(self):
        self.dishes: List[Dish] = [
            DishFactory.create() for _ in range(random.randint(1, 10))
        ]

    def tearDown(self):
        for dish in self.dishes:
            dish.delete()

    def test_create_service(self):
        """Test creating a new service."""
        response = self.client.post(
            reverse("orders:orders-create"),
            {
                "table_number": random.randint(1, 1000),
                "items": [dish.pk for dish in self.dishes],
            },
        )

        self.assertRedirects(response, reverse("orders:orders-list"))


class OrderUpdateViewTest(TestCase):
    """Test case class for testing OrderUpdateView."""

    def setUp(self):
        self.dishes: List[Dish] = [
            DishFactory.create() for _ in range(random.randint(1, 10))
        ]
        self.order: Order = OrderFactory.create(items=self.dishes)

    def tearDown(self):
        for dish in self.dishes:
            dish.delete()
        self.order.delete()

    def test_update_order(self):
        """Test updating the order."""
        new_status: str = random.choice(list(Order.STATUSES.keys()))

        response = self.client.post(
            reverse(
                "orders:orders-update",
                kwargs={"pk": self.order.pk},
            ),
            {
                "status": new_status,
            },
        )

        # Check redirect
        self.assertRedirects(
            response,
            reverse(
                "orders:orders-detail",
                kwargs={"pk": self.order.pk},
            ),
        )
        # Check that the old primary key contains updated data
        order_ = Order.objects.filter(pk=self.order.pk).first()
        self.assertEqual(order_.status, new_status)


class OrderDeleteViewTest(TestCase):
    """Test case class for testing OrderDeleteView."""

    def setUp(self):
        self.dishes: List[Dish] = [
            DishFactory.create() for _ in range(random.randint(1, 10))
        ]
        self.order: Order = OrderFactory.create(items=self.dishes)

    def tearDown(self):
        for dish in self.dishes:
            dish.delete()
        self.order.delete()

    def test_delete_order(self):
        """Test deleting the order."""
        response = self.client.post(
            reverse(
                "orders:orders-delete",
                kwargs={"pk": self.order.pk},
            )
        )

        # Check redirect
        self.assertRedirects(response, reverse("orders:orders-list"))
        # Check that there is no data for the old primary key
        not_existing_order = Order.objects.filter(pk=self.order.pk).first()
        self.assertIsNone(not_existing_order)

"""Module with factories."""

import random

import factory.fuzzy

from .models import Order

STATUSES = ("в ожидании", "готово", "оплачено")


class OrderFactory(factory.django.DjangoModelFactory):
    """Lead factory."""

    class Meta:
        """Meta class."""

        model = Order

    table_number: factory.LazyAttribute = factory.LazyAttribute(
        lambda n: random.randint(1, 1000)
    )
    status: factory.LazyAttribute = factory.LazyAttribute(
        lambda status: random.choice(STATUSES)
    )

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        """Add items to order."""
        if not create or not extracted:
            return

        self.items.add(*extracted)  # type: ignore[attr-defined]

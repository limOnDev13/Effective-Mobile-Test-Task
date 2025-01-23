"""Module with factories."""

import random

import factory.fuzzy

from .models import Dish


class DishFactory(factory.django.DjangoModelFactory):
    """Dish factory class."""

    class Meta:
        """Meta class."""

        model = Dish  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ("name", "description", "price")

    name = factory.faker.Faker("word")
    description = factory.faker.Faker("text")
    price = factory.LazyAttribute(lambda x: round(random.uniform(0, 100), 2))

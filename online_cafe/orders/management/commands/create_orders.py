import random
from typing import List

from django.core.management import BaseCommand
from menu.factories import DishFactory
from menu.models import Dish
from orders.factories import OrderFactory


class Command(BaseCommand):
    help = "Create random orders with random dishes."

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of orders")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random orders...")

        # create dishes
        dishes: List[Dish] = list()
        for _ in range(random.randint(10, 20)):
            dish = DishFactory.create()
            dishes.append(dish)

        for num in range(count):
            OrderFactory.create(items=random.choices(dishes, k=random.randint(1, 10)))

        self.stdout.write(f"Done")

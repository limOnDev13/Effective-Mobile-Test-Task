from django.core.management import BaseCommand
from menu.factories import DishFactory


class Command(BaseCommand):
    help = "Create random dishes."

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of dishes")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random dishes...")

        for num in range(count):
            dish = DishFactory.create()
            self.stdout.write(
                f"Create #{num} service:\n"
                f"pk={dish.pk} name={dish.name}"
                f" price={dish.price} description:\n{dish.description}\n"
            )

        self.stdout.write(f"Done")

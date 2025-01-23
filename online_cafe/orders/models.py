"""Module with ORM models."""

from django.db import models
from django.core.validators import MinValueValidator
from menu.models import Dish


class Order(models.Model):
    """ORM representation of the table of orders."""

    id = models.IntegerField(primary_key=True)
    table_number = models.IntegerField(null=False, help_text="Номер стола", validators=[MinValueValidator(0)])
    items = models.ManyToManyField(Dish, help_text="Список блюд в заказе")
    status = models.CharField(
        choices=("в ожидании", "готово", "оплачено"),
        help_text="Статус заказа: “в ожидании”, “готово”, “оплачено”",
        default="в ожидании"
    )

    @property
    def total_price(self) -> float:
        """Get total price."""
        return sum(self.items_set.values_list("price", flat=True))

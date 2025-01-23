"""Module with ORM models."""

from django.db import models
from django.core.validators import MinValueValidator
from menu.models import Dish


class Order(models.Model):
    """ORM representation of the table of orders."""

    table_number = models.IntegerField(null=False, verbose_name="Номер стола", validators=[MinValueValidator(0)])
    items = models.ManyToManyField(Dish, verbose_name="Список блюд в заказе")
    status = models.CharField(
        choices={
            "pending": "в ожидании",
            "done": "готово",
            "paid": "оплачено",
        },
        verbose_name="Статус заказа",
        default="в ожидании"
    )

    @property
    def total_price(self) -> float:
        """Get total price."""
        return sum(self.items.values_list("price", flat=True))

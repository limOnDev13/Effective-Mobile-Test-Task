"""Module with ORM models."""

from typing import Dict

from django.core.validators import MinValueValidator
from django.db import models
from menu.models import Dish


class Order(models.Model):
    """ORM representation of the table of orders."""

    STATUSES: Dict[str, str] = {
        "done": "готово",
        "paid": "оплачено",
        "pending": "в ожидании",
    }

    table_number: models.IntegerField = models.IntegerField(
        null=False, verbose_name="Номер стола", validators=[MinValueValidator(0)]
    )
    items: models.ManyToManyField = models.ManyToManyField(
        Dish, verbose_name="Список блюд в заказе"
    )
    status: models.CharField = models.CharField(
        choices=STATUSES,
        verbose_name="Статус заказа",
        default="в ожидании",
    )

    class Meta:
        """Meta class."""

        ordering = ["pk"]

    @property
    def total_price(self) -> float:
        """Get total price."""
        return sum(self.items.values_list("price", flat=True))

    def __str__(self) -> str:
        """Return string representation of the model."""
        return f"Заказ #{self.pk} - стол №{self.table_number}"

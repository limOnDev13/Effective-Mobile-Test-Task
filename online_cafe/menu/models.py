"""Module with ORM models."""

from django.db import models


class Dish(models.Model):
    """ORM representation of the table of dishes."""

    name = models.CharField(
        max_length=30, blank=False, null=False, help_text="Название блюда"
    )
    description = models.TextField(null=True, blank=True, help_text="Описание блюда")
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, help_text="Цена блюда")

    class Meta:
        """Class Meta."""

        verbose_name_plural = "Dishes"

    def __str__(self) -> str:
        """Return the string representation of the model."""
        return f"{self.name} ({self.pk}) - {self.price}"

"""Class with Views."""

from typing import List

from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Order


class OrderCreateView(CreateView):
    """Create view class for Order."""

    model = Order
    fields = "table_number", "items"
    success_url = reverse_lazy("orders:orders-list")
    template_name = "orders/orders-create.html"


class OrderListView(ListView):
    """List view class for Order."""

    template_name = "orders/orders-list.html"
    context_object_name = "orders"

    @classmethod
    def __filter_status(cls, statuses: List[str]):
        """
        Add up the status filters bitwise.

        :param statuses: List of statuses from GET params.
        :return: Q(status=status[0]) | Q(status=status[1]) |...
        """
        result = Q(status=statuses[0])
        for i in range(1, len(statuses)):
            result = result | Q(status=statuses[i])
        return result

    def get_queryset(self):
        """Get a queryset depending on the GET parameters."""
        table_number = self.request.GET.get("table_number")
        statuses = self.request.GET.getlist("status")
        if not statuses and not table_number:
            return Order.objects.prefetch_related("items")
        elif not statuses:
            return Order.objects.prefetch_related("items").filter(
                table_number=table_number
            )
        elif not table_number:
            return Order.objects.prefetch_related("items").filter(
                self.__filter_status(statuses)
            )
        else:
            return Order.objects.prefetch_related("items").filter(
                Q(table_number=table_number) & self.__filter_status(statuses)
            )


class OrderDetailView(DetailView):
    """Detail view class for Order."""

    queryset = Order.objects.prefetch_related("items")
    template_name = "orders/orders-detail.html"
    context_object_name = "order"


class OrderUpdateView(UpdateView):
    """Update view class for Order."""

    model = Order
    fields = ("status", "items")
    template_name = "orders/orders-update.html"

    def get_success_url(self):
        """Return success redirect url."""
        return reverse(
            "orders:orders-detail",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(DeleteView):
    """Delete view class for Order."""

    model = Order
    success_url = reverse_lazy("orders:orders-list")
    template_name = "orders/orders-delete.html"


def get_revenue_per_shift(request: HttpRequest) -> HttpResponse:
    """Get revenue per shift."""
    paid_orders = Order.objects.filter(status="оплачено").all()
    revenue = sum(order.total_price for order in paid_orders)
    context = {"revenue": revenue, "orders": paid_orders}
    return render(request, "orders/orders-revenue.html", context=context)

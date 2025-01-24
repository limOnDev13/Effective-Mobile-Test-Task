"""Class with Views."""

from django.db.models import Q
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

    def get_queryset(self):
        """Get a queryset depending on the GET parameters."""
        table_number = self.request.GET.get("table_number")
        status = self.request.GET.get("status")

        if not status and not table_number:
            return Order.objects.prefetch_related("items")
        elif not status:
            return Order.objects.prefetch_related("items").filter(
                table_number=table_number
            )
        elif not table_number:
            return Order.objects.prefetch_related("items").filter(status=status)
        else:
            return Order.objects.prefetch_related("items").filter(
                Q(table_number=table_number) & Q(status=status)
            )


class OrderDetailView(DetailView):
    """Detail view class for Order."""

    queryset = Order.objects.prefetch_related("items")
    template_name = "orders/orders-detail.html"
    context_object_name = "order"


class OrderUpdateView(UpdateView):
    """Update view class for Order."""

    model = Order
    fields = ("status",)
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

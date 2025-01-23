"""Class with Views."""

from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from .models import Order


class OrderCreateView(CreateView):
    model = Order
    fields = "table_number", "items"
    success_url = reverse_lazy("orders:orders_list")
    template_name = "orders/orders-create.html"


class OrderListView(ListView):
    queryset = Order.objects.prefetch_related("items")
    template_name = "orders/orders-list.html"
    context_object_name = "orders"

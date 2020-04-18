from .models import Order
from django.urls import reverse
import random


def get_order(request, cartshop):
    order = cartshop.order

    if not order and request.user.is_authenticated:
        order = Order.objects.create(cartshop=cartshop, user=request.user)

    if order:
        request.session['order_id'] = order.order_id

    return order


def breadcrumb(products=True, address=False, payment=False, confirmation=False):
    return [
        {'title': 'Products', 'active': products, 'url': reverse('orders:order')},
        {'title': 'Addresses', 'active': address, 'url': reverse('orders:address')},
        {'title': 'Payment', 'active': payment, 'url': reverse('orders:order')},
        {'title': 'Confirm', 'active': confirmation, 'url': reverse('orders:order')}
    ]


def get_shipping_cost(order, cartshop):
    return random.randrange(5, 101, 2)  # Even integer from 5 to 100


def destroy_order(request):
    request.session['order_id'] = None

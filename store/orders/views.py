from django.shortcuts import render, redirect, get_object_or_404
from cartshop.helper import get_cartshop
from .helper import get_order, get_shipping_cost
from django.contrib.auth.decorators import login_required
from .helper import breadcrumb, destroy_order
from cartshop.helper import destroy_cartshop
from shipping_addresses.models import ShippingAddress
from django.contrib import messages


@login_required(login_url='login')
def order(request):
    cartshop = get_cartshop(request)
    order = get_order(request, cartshop)
    if order.shipping_total == 0:
        order.shipping_total = get_shipping_cost(order, cartshop)
        order.save()

    return render(request, 'orders/order.html', {'order': order,
                                                 'cart': cartshop,
                                                 'breadcrumb': breadcrumb()})


@login_required(login_url='login')
def address(request):
    cartshop = get_cartshop(request)
    order = get_order(request, cartshop)
    shipping_address = order.get_or_set_shipping_address()
    can_choose_address = request.user.shippingaddress_set.count() > 1

    return render(request, 'orders/address.html', {
        'can_choose_address': can_choose_address,
        'cart': cartshop, 'order': order, 'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(address=True)})

@login_required(login_url='login')
def select_address(request):
    shipping_addresses = request.user.shippingaddress_set.all()

    return render(request, 'orders/select_address.html', {
        'shipping_addresses': shipping_addresses,
        'breadcrumb': breadcrumb(address=True)})


@login_required(login_url='login')
def set_address(request, id):
    cartshop = get_cartshop(request)
    order = get_order(request, cartshop)

    shipping_address = get_object_or_404(ShippingAddress, pk=id)

    if request.user.id != shipping_address.user_id:
        return redirect('cartshop:cartshop')

    order.update_shipping_address(shipping_address)
    return redirect('orders:address')


@login_required(login_url='login')
def confirm(request):
    cartshop = get_cartshop(request)
    order = get_order(request, cartshop)

    shipping_address = order.shipping_address
    if not shipping_address:
        return redirect('orders:address')

    return render(request, 'orders/confirm.html', {
        'cartshop': cartshop,
        'order': order,
        'shipping_address': shipping_address, 
        'breadcrumb': breadcrumb(address=True, confirmation=True)
    })


@login_required(login_url='login')
def cancel(request):
    cartshop = get_cartshop(request)
    order = get_order(request, cartshop)

    if request.user.id != order.user_id:
        return redirect('cartshop:cartshop')

    order.cancel()
    destroy_cartshop(request)
    destroy_order(request)

    messages.error(request, "Order canceled")
    return redirect('index')


@login_required(login_url='login')
def complete(request):
    cartshop = get_cartshop(request)
    order = get_order(request, cartshop)

    if request.user.id != order.user_id:
        return redirect('cartshop:cartshop')

    order.complete()
    destroy_cartshop(request)
    destroy_order(request)    
    messages.success(request, "Order completed successfully")

    return redirect('index')

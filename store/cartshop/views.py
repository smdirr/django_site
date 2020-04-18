from django.shortcuts import render, redirect, get_object_or_404
from .helper import get_cartshop
from products.models import Product
from .models import CartProducts


def cartshop(request):
    cart = get_cartshop(request)
    return render(request, 'cartshops/cartshop.html', {'cart': cart})


def add(request):
    cart = get_cartshop(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1))
    cp = CartProducts.objects.set_quantity(cartshop=cart,
                                           product=product,
                                           quantity=quantity)
    return render(request, 'cartshops/addcart.html', {
        'cp': cp,
        'quantity': quantity,
        'product': product})


def remove(request):
    cart = get_cartshop(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    cart.products.remove(product)
    return redirect('cartshop:cartshop')

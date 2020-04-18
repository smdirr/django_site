from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import ShippingAddress
from .forms import ShippingAddressForm
from cartshop.helper import get_cartshop
from orders.helper import get_order


class ShippingAddressListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_address/shipping_address.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-principal')


class ShippingAddressUpdatedView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'shipping_address/update.html'
    success_message = 'Address updated successfully '

    def get_success_url(self):
        return reverse('shipping_addresses:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            return redirect('cartshop:cartshop')
        return super(ShippingAddressUpdatedView, self).dispatch(request, *args, **kwargs)


class ShippingAddressDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_address/delete.html'
    success_url = reverse_lazy('shipping_addresses:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().principal:
            return redirect('shipping_addresses:shipping_addresses')
        if request.user.id != self.get_object().user_id:
            return redirect('cartshop:cartshop')
        if self.get_object().has_orders():
            messages.warning(request, "This address cannot be removed because it was used in an order")
            return redirect('shipping_addresses:shipping_addresses')
        return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)


@login_required(login_url='login')
def create(request):
    form = ShippingAddressForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        shipping_address.principal = not request.user.has_shipping_address()
        shipping_address.save()

        if request.GET.get('next'):
            if request.GET['next'] == reverse('orders:address'):
                cartshop = get_cartshop(request)
                order = get_order(request, cartshop)
                order.update_shipping_address(shipping_address)
                return HttpResponseRedirect(request.GET['next'])

        messages.success(request, "Address added successfully")
        return redirect('shipping_addresses:shipping_addresses')
    return render(request, 'shipping_address/create.html', {'form': form})


def principal(request, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('cartshop:cartshop')

    if request.user.has_shipping_address():
        request.user.shipping_address.update_principal()
    shipping_address.update_principal(True)
    return redirect('shipping_addresses:shipping_addresses')

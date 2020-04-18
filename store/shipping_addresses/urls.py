from django.urls import path
from . import views


app_name = 'shipping_addresses'

urlpatterns = [
    path('', views.ShippingAddressListView.as_view(), name='shipping_addresses'),
    path('new', views.create, name='create'),
    path('edit/<int:pk>', views.ShippingAddressUpdatedView.as_view(), name='edit'),
    path('delete/<int:pk>', views.ShippingAddressDeleteView.as_view(), name='delete'),
    path('principal/<int:pk>', views.principal, name='principal')
]

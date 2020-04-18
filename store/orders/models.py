import uuid
from django.db import models
from users.models import User
from cartshop.models import CartShop
from enum import Enum
from django.db.models.signals import pre_save
from shipping_addresses.models import ShippingAddress


class OrderStatus(Enum):
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'


status_choices = [(tag, tag.value) for tag in OrderStatus]


class Order(models.Model):
    order_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cartshop = models.ForeignKey(CartShop, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=status_choices,
                              default=OrderStatus.CREATED)
    shipping_total = models.DecimalField(default=0, max_digits=8, 
                                         decimal_places=2)
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippingAddress, null=True, blank=True, 
                                         on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id

    def cancel(self):
        self.status = OrderStatus.CANCELED
        self.save()

    def complete(self):
        self.status = OrderStatus.COMPLETED
        self.save()

    def get_or_set_shipping_address(self):
        if self.shipping_address:
            return self.shipping_address
        _shipping_address = self.user.shipping_address
        if _shipping_address:
            self.update_shipping_address(_shipping_address)

        return _shipping_address

    def update_total(self):
        self.total = self.get_total()
        self.save()

    def get_total(self):
        return self.cartshop.total + self.shipping_total

    def update_shipping_address(self, _shipping_address):
        self.shipping_address = _shipping_address
        self.save()


def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())


def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()


pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)

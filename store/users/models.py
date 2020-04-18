from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def get_full_name(self):
        return '{}, {}'.format(self.last_name, self.first_name)

    @property
    def shipping_address(self):
        return self.shippingaddress_set.filter(principal=True).first()

    def has_shipping_address(self):
        return self.shipping_address is not None


class Customer(User):
    class Meta:
        proxy = True

    def get_products(self):
        return []


class Profile(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    description = models.TextField()

from django.db import models
from users.models import User


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    reference = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=20, null=False, blank=False)
    principal = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.zip_code

    @property
    def address(self):
        return "{} - {} - {}".format(self.city, self.state, self.country)

    def update_principal(self, principal=False):
        self.principal = principal
        self.save()

    def has_orders(self):
        return self.order_set.count() > 0

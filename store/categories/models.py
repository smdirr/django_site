from django.db import models
from products.models import Product


class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    products = models.ManyToManyField(Product)
    
    def __str__(self):
        return self.title

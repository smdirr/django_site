from django.contrib import admin
from .models import Product
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'price', 'image')
    list_display = ('title', 'description', 'price', 'slug', 'created')


admin.site.register(Product, ProductAdmin)

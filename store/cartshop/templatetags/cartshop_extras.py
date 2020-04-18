from django import template

register = template.Library()


@register.filter()
def quantity_products_format(quantity=1):
    return '{} {}'.format(quantity, 'products' if quantity > 1 else 'product')

from django import template

register = template.Library()

@register.filter()
def price_format(value):
    return '€{0:.2f}'.format(value)

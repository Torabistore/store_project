# catalog/templatetags/price_filters.py
from django import template

register = template.Library()

@register.filter
def price_format(value):
    """
    فرمت عدد را به صورت 1.234.567 برمی‌گرداند
    """
    try:
        value = int(value)
        return "{:,}".format(value).replace(",", ".")
    except (ValueError, TypeError):
        return value

from django import template

register = template.Library()

@register.filter()
def price_format(value):
    try:
        value = float(value)
        formatted = f"{value:,.0f}"
        return f"{formatted} تومان"
    except (ValueError, TypeError):
        return "نامشخص"

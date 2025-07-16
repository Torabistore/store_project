from django import template

register = template.Library()

@register.filter
def price_format(value):
    """فرمت‌دهی قیمت به صورت عدد با کاما و 'تومان'"""
    try:
        value = int(value)
        return f"{value:,} تومان"
    except (ValueError, TypeError):
        return "قیمت نامعتبر"

from django import template

register = template.Library()

@register.filter
def split_by_newline(value):
    """
    Splits a string by newline characters and returns a list of strings.
    Useful for displaying multi-line text as list items.
    """
    if value:
        return value.split('\n')
    return []

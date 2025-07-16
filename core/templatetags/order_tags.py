from django import template

register = template.Library()

@register.filter
def status_color(status):
    colors = {
        'pending': 'warning',
        'processing': 'info',
        'shipped': 'success',
        'cancelled': 'danger',
    }
    return colors.get(status, 'secondary')

# catalog/context_processors.py

from .models import Product

def categories(request):
    cats = Product.objects.values_list('category', flat=True).distinct().order_by('category')
    current = request.resolver_match.kwargs.get('category_name') if request.resolver_match else None
    return {
        'categories': cats,
        'current_category': current
    }

from .models import Category

def categories(request):
    cats = Category.objects.all().order_by('name')
    current = request.resolver_match.kwargs.get('slug') if request.resolver_match else None
    return {
        'categories': cats,
        'current_category': current
    }

# catalog/views.py

from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def homepage(request):
    recent_products = Product.objects.all().order_by('-created_at')[:8]
    return render(request, 'catalog/homepage.html', {'recent_products': recent_products})

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    page_obj = products 
    return render(request, 'catalog/product_list.html', {'page_obj': page_obj, 'categories': categories})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    page_obj = products
    return render(request, 'catalog/product_list.html', {
        'category': category,
        'page_obj': page_obj,
        'categories': categories,
        'title': f'محصولات دسته {category.name}'
    })

# =========== ویو جدید برای صفحه "درباره ما" ===========
def about_page(request): # <--- این تابع اضافه شد
    return render(request, 'catalog/about_page.html')

# =========== ویو جدید برای صفحه "تماس با ما" ===========
def contact_page(request): # <--- این تابع اضافه شد
    return render(request, 'catalog/contact_page.html')
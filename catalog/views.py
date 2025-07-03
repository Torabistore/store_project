# D:\store_project\catalog\views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Category
from .forms import ContactForm

def homepage(request):
    recent_products = Product.objects.all().order_by('-created_at')[:8]
    categories = Category.objects.all()  # اضافه شده برای پاس دادن دسته‌بندی‌ها به قالب
    return render(request, 'catalog/homepage.html', {
        'recent_products': recent_products,
        'categories': categories,
    })

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    page_obj = products
    return render(request, 'catalog/product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()  # اضافه شده برای ناوبری دسته‌ها
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'categories': categories,
    })

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    page_obj = products
    return render(request, 'catalog/product_list.html', {
        'category': category,
        'page_obj': page_obj,
        'categories': categories,
        'title': f'محصولات دسته {category.name}',
    })

def about_page(request):
    categories = Category.objects.all()
    return render(request, 'catalog/about_page.html', {
        'categories': categories,
    })

def contact_page(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'پیام شما با موفقیت ارسال شد!')
            return redirect('catalog:contact_page')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را برطرف کنید.')
    else:
        form = ContactForm()
    return render(request, 'catalog/contact_page.html', {
        'form': form,
        'categories': categories,
    })
def search_results(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.none()
    categories = Category.objects.all()
    return render(request, 'catalog/search_results.html', {
        'page_obj': products,
        'categories': categories,
        'query': query,
    })


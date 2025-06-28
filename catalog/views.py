# catalog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Q
from django.core.paginator import Paginator

def homepage(request):
    categories = Product.objects.values_list('category', flat=True).distinct().order_by('category')
    newest_products = Product.objects.order_by('-id')[:6]
    featured_categories = []
    for cat_name in categories:
        product_in_category = Product.objects.filter(category=cat_name).exclude(image='').first()
        if product_in_category:
            featured_categories.append({'name': cat_name, 'image_url': product_in_category.image.url})
    context = {'categories': categories, 'newest_products': newest_products, 'featured_categories': featured_categories}
    return render(request, 'catalog/homepage.html', context)

def product_list(request, category_name=None):
    categories = Product.objects.values_list('category', flat=True).distinct().order_by('category')
    products_list = Product.objects.all().order_by('name')
    if category_name:
        products_list = products_list.filter(category=category_name)
    paginator = Paginator(products_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'categories': categories, 'current_category': category_name}
    return render(request, 'catalog/product_list.html', context)

# تابع جزئیات محصول با منطق جدید
def product_detail(request, pk):
    categories = Product.objects.values_list('category', flat=True).distinct().order_by('category')
    product = get_object_or_404(Product, pk=pk)

    # ---- بخش جدید برای پیدا کردن محصولات مشابه ----
    # محصولاتی را پیدا کن که در همین دسته‌بندی هستند،
    # خود محصول فعلی را از لیست حذف کن،
    # و در نهایت ۴ تای اول را انتخاب کن.
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    # ---------------------------------------------

    context = {
        'product': product,
        'categories': categories,
        'related_products': related_products, # لیست محصولات مشابه را هم به تمپلیت می‌فرستیم
    }
    return render(request, 'catalog/product_detail.html', context)

def search_results(request):
    categories = Product.objects.values_list('category', flat=True).distinct().order_by('category')
    query = request.GET.get('q', None)
    if query:
        products_list = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(brand__icontains=query) | Q(sku__icontains=query)).distinct()
    else:
        products_list = Product.objects.none()
    paginator = Paginator(products_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'categories': categories, 'query': query}
    return render(request, 'catalog/product_list.html', context)

def about_page(request):
    categories = Product.objects.values_list('category', flat=True).distinct().order_by('category')
    context = {'categories': categories}
    return render(request, 'catalog/about.html', context)

def contact_page(request):
    categories = Product.objects.values_list('category', flat=True).distinct().order_by('category')
    context = {'categories': categories}
    return render(request, 'catalog/contact.html', context)
# این دو تابع را به انتهای catalog/views.py اضافه کنید

def about_page(request):
    return render(request, 'catalog/about.html')

def contact_page(request):
    return render(request, 'catalog/contact.html')
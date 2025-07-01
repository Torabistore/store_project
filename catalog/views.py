# D:\store_project\catalog\views.py

from django.shortcuts import render, get_object_or_404, redirect # اضافه شدن redirect
from django.contrib import messages # اضافه شدن messages
from .models import Product, Category
from .forms import ContactForm # <--- این خط اضافه شد

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

def about_page(request): 
    return render(request, 'catalog/about_page.html')

# =========== ویو جدید برای صفحه "تماس با ما" ===========
def contact_page(request): # <--- این تابع تغییر کرد
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # اینجا میتونی کارهایی مثل ارسال ایمیل، ذخیره در دیتابیس و ... انجام بدی
            # مثلاً: send_mail(form.cleaned_data['subject'], form.cleaned_data['message'], form.cleaned_data['email'], ['info@torabistore.com'])
            messages.success(request, 'پیام شما با موفقیت ارسال شد!')
            return redirect('catalog:contact_page') # بعد از ارسال موفق، ریدایرکت به همین صفحه
        else:
            messages.error(request, 'لطفاً خطاهای فرم را برطرف کنید.')
    else:
        form = ContactForm()
    return render(request, 'catalog/contact_page.html', {'form': form})
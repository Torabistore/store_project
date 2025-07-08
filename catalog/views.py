from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, Category
from accounts.models import Order, OrderItem
from .forms import ContactForm

def homepage(request):
    recent_products = Product.objects.filter(available=True).order_by('-created_at')[:4]
    return render(request, 'catalog/homepage.html', {'recent_products': recent_products})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('id')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/product_list.html', {
        'category': category,
        'categories': categories,
        'products': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, available=True)
    return render(request, 'catalog/product_detail.html', {'product': product})

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    order = Order.objects.filter(user=request.user, status='pending').first()
    return render(request, 'catalog/cart.html', {'order': order})

def cart_add(request, product_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    product = get_object_or_404(Product, id=product_id, available=True)
    order, created = Order.objects.get_or_create(user=request.user, status='pending')
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={'price': product.price}
    )
    if not created:
        order_item.quantity += 1
        order_item.save()

    order.total_price = sum(item.price * item.quantity for item in order.items.all())
    order.save()

    messages.success(request, f'{product.name} به سبد خرید اضافه شد.')
    return redirect('catalog:cart_view')

def cart_remove(request, item_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__status='pending')
    order = order_item.order
    order_item.delete()
    order.total_price = sum(item.price * item.quantity for item in order.items.all())
    order.save()
    messages.success(request, 'محصول از سبد خرید حذف شد.')
    return redirect('catalog:cart_view')

def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    order = Order.objects.filter(user=request.user, status='pending').first()
    if not order:
        messages.error(request, "سبد خرید شما خالی است.")
        return redirect('catalog:product_list')

    if request.method == 'POST':
        messages.success(request, "سفارش شما ثبت شد.")
        order.status = 'processing'
        order.save()
        return redirect('catalog:homepage')

    return render(request, 'catalog/checkout.html', {'order': order})

def search_results(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query, available=True).order_by('id')
    return render(request, 'catalog/search_results.html', {'products': products, 'query': query})

def about_page(request):
    return render(request, 'catalog/about_page.html')

def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message_content = form.cleaned_data['message']
            messages.success(request, 'پیام شما با موفقیت ارسال شد. از تماس شما سپاسگزاریم!')
            return redirect('catalog:contact_page')
        else:
            messages.error(request, 'لطفاً اطلاعات را به درستی وارد کنید.')
    else:
        form = ContactForm()
    return render(request, 'catalog/contact_page.html', {'form': form})

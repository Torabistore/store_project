from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product, Category, Order, PaymentRequest  # فرض بر وجود این مدل‌هاست
from users.models import Profile


# 🏠 صفحه اصلی و لیست محصولات
def homepage_view(request):
    products = Product.objects.filter(available=True)
    return render(request, 'catalog/homepage.html', {'products': products})


def product_list_view(request):
    products = Product.objects.filter(available=True)
    return render(request, 'catalog/product_list.html', {'products': products})


def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'catalog/product_detail.html', {'product': product})


# 🔍 جستجو
def search_results(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'catalog/search_results.html', {
        'products': products,
        'query': query
    })


# 📬 صفحه تماس
def contact_page_view(request):
    return render(request, 'catalog/contact.html')


# 📦 نمایش سفارش‌های کاربر
@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'catalog/order_list.html', {'orders': orders})


# 🗂 نمایش محصولات یک دسته‌بندی
def category_products_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    return render(request, 'catalog/category_products.html', {
        'category': category,
        'products': products
    })


# 💳 ثبت درخواست پرداخت
@login_required
def submit_payment_view(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))
        receipt = request.FILES.get('receipt')
        description = request.POST.get('description', '')
        tracking_code = request.POST.get('tracking_code', '')

        if amount >= 1000:
            PaymentRequest.objects.create(
                user=request.user,
                amount=amount,
                payment_receipt=receipt,
                description=description,
                reference_number=tracking_code,
                status='pending'
            )
            messages.success(request, "پرداخت شما با موفقیت ثبت شد ✅")
        else:
            messages.error(request, "مبلغ باید حداقل ۱۰۰۰ باشد ❌")

        return redirect('catalog:submit_payment')

    return render(request, 'catalog/submit_payment.html')


# ✅ تأیید/رد درخواست پرداخت
@login_required
def approve_payment(request, pk):
    payment = get_object_or_404(PaymentRequest, pk=pk)
    payment.status = 'approved'
    payment.save()
    messages.success(request, "پرداخت تأیید شد ✅")
    return redirect('catalog:payment_list_admin')


@login_required
def reject_payment(request, pk):
    payment = get_object_or_404(PaymentRequest, pk=pk)
    payment.status = 'rejected'
    payment.save()
    messages.error(request, "پرداخت رد شد ❌")
    return redirect('catalog:payment_list_admin')


# 🛒 سبد خرید (کمترین پیاده‌سازی برای رفع ImportError)
@login_required
def cart_view(request):
    # TODO: جایگزین با منطق واقعی سبد (session یا مدل)
    cart = request.session.get('cart', {})
    return render(request, 'catalog/cart.html', {'cart': cart})


@login_required
def add_to_cart_view(request, product_id):
    cart = request.session.setdefault('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session.modified = True
    return redirect('catalog:cart_view')


@login_required
def cart_increase_view(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session.modified = True
    return redirect('catalog:cart_view')


@login_required
def cart_decrease_view(request, product_id):
    cart = request.session.get('cart', {})
    qty = cart.get(str(product_id), 0) - 1
    if qty > 0:
        cart[str(product_id)] = qty
    else:
        cart.pop(str(product_id), None)
    request.session.modified = True
    return redirect('catalog:cart_view')


@login_required
def cart_remove_view(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session.modified = True
    return redirect('catalog:cart_view')


# 🛒 نهایی‌سازی پرداخت
@login_required
def checkout_view(request):
    # TODO: پیاده‌سازی واقعی پرداخت و ایجاد Order
    messages.info(request, "درگاه پرداخت شبیه‌سازی شد.")
    request.session.pop('cart', None)
    return redirect('catalog:homepage')

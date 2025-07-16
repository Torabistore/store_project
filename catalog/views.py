from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from catalog.models import Product, Category, PaymentRequest
from core.models import Order, CartItem
from core.forms import PaymentRequestForm




def homepage_view(request):
    recent_products = Product.objects.filter(available=True).order_by('-created_at')[:8]
    return render(request, 'catalog/homepage.html', {
        'recent_products': recent_products
    })


# ✅ لیست محصولات
def product_list_view(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    return render(request, 'catalog/product_list.html', {
        'products': products,
        'categories': categories,
    })

# ✅ جزئیات محصول
def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'catalog/product_detail.html', {'product': product})

# ✅ لیست سفارش‌های کاربر
@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/order_list.html', {'orders': orders})

# ✅ جزئیات سفارش خاص
@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'catalog/order_detail.html', {'order': order})

# ✅ سبد خرید
@login_required
def cart_view(request):
    cart = request.session.get('cart', {})  # {'2': 1, '7': 3}
    items = []
    total_price = 0

    for product_id_str, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id_str))
            item_total = product.price * quantity

            items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price,
                'total': item_total
            })
            total_price += item_total
        except Product.DoesNotExist:
            continue

    return render(request, 'catalog/cart.html', {
        'items': items,
        'total_price': total_price,
    })


# ✅ صفحه تماس
def contact_page_view(request):
    return render(request, 'catalog/contact.html')

# ✅ جستجو
def search_results(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'catalog/search_results.html', {
        'query': query,
        'results': results,
    })

# ✅ محصولات یک دسته‌بندی
def category_products_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'catalog/product_list.html', {
        'products': products,
        'categories': categories,
        'active_category': category,
    })
# ✅ افزودن به سبد خرید (ایمن با بررسی نوع درخواست)
def add_to_cart_view(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1

        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        request.session['cart'] = cart

        return redirect('catalog:cart_view')

    # ⛔ اگر درخواست غیر POST بود، کاربر برگرده به جزئیات محصول
    return redirect('catalog:product_detail', product_id)

# ✅ ثبت درخواست پرداخت
@login_required
def submit_payment_view(request):
    print("⚡ ویوی ثبت پرداخت صدا زده شد")

    if request.method == 'POST':
        print("📥 فرم ارسال شد با داده‌ها:", request.POST.dict())
        print("📎 فایل فیش دریافتی:", request.FILES.get('receipt'))

        amount = request.POST.get('amount')
        receipt = request.FILES.get('receipt')
        description = request.POST.get('description')
        tracking_code = request.POST.get('tracking_code')

        try:
            amount_val = float(amount) if amount else None
            if amount_val and amount_val >= 1000 and receipt:
                PaymentRequest.objects.create(
                    user=request.user,
                    amount=amount_val,
                    payment_receipt=receipt,
                    description=description,
                    reference_number=tracking_code,
                    status='pending'
                )
                print("✅ پرداخت ثبت شد")
                messages.success(request, "پرداخت شما با موفقیت ثبت شد ✅")
            else:
                messages.error(request, "مبلغ نامعتبر یا فایل فیش انتخاب نشده ❌")
        except Exception as e:
            print("❌ خطا در ثبت پرداخت:", str(e))
            messages.error(request, "ثبت پرداخت با خطا مواجه شد ❌")

        return redirect('catalog:submit_payment')

    return render(request, 'catalog/submit_payment.html')

# ✅ تأیید پرداخت (توسط ادمین)
@staff_member_required
def approve_payment(request, pk):
    req = get_object_or_404(PaymentRequest, pk=pk)
    req.approve()
    return redirect('/admin/catalog/paymentrequest/')

# ✅ رد پرداخت (توسط ادمین)
@staff_member_required
def reject_payment(request, pk):
    req = get_object_or_404(PaymentRequest, pk=pk)
    req.status = 'rejected'
    req.save()
    return redirect('/admin/catalog/paymentrequest/')

@login_required
def cart_increase_view(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('catalog:cart_view')


@login_required
def cart_decrease_view(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] = max(cart[str(product_id)] - 1, 1)
        request.session['cart'] = cart
    return redirect('catalog:cart_view')


@login_required
def cart_remove_view(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('catalog:cart_view')


@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})  # {'2': 1, '7': 3}
    items = []
    total_price = 0

    for product_id_str, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id_str))
            item_total = product.price * quantity
            items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price,
                'total': item_total
            })
            total_price += item_total
        except Product.DoesNotExist:
            continue

    return render(request, 'catalog/checkout.html', {
        'cart': items,
        'total_price': total_price,
    })




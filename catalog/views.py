from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductVariant, Category
from django.contrib import messages

# صفحه اصلی
def homepage(request):
    products = Product.objects.order_by('-created_at')[:8]
    return render(request, 'catalog/homepage.html', {'recent_products': products})


# لیست محصولات
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'catalog/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


# جزئیات محصول
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, available=True)
    return render(request, 'catalog/product_detail.html', {'product': product})


# افزودن به سبد خرید
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variant_id = request.POST.get("variant_id")
    quantity = int(request.POST.get("quantity", 1))

    if quantity < 1:
        messages.warning(request, "تعداد وارد شده معتبر نیست.")
        return redirect('catalog:product_detail', pk=product.id)

    cart = request.session.get('cart', [])
    cart.append({
        'product_id': product.id,
        'variant_id': int(variant_id) if variant_id else None,
        'quantity': quantity
    })
    request.session['cart'] = cart
    messages.success(request, "محصول به سبد خرید افزوده شد.")
    return redirect('catalog:cart_view')


# نمای سبد خرید
def cart_view(request):
    cart = request.session.get('cart', [])
    items = []
    total_price = 0

    for item in cart:
        product = get_object_or_404(Product, id=item['product_id'])
        variant = None
        price = product.price

        if item['variant_id']:
            variant = get_object_or_404(ProductVariant, id=item['variant_id'], product=product)
            price = variant.price

        total_price += price * item['quantity']
        items.append({
    'product': product,
    'variant': variant,
    'quantity': item['quantity'],
    'price': price,
    'total': price * item['quantity']  # ✨ اضافه‌شده
})


    return render(request, 'catalog/cart.html', {
        'items': items,
        'total_price': total_price
    })


# حذف آیتم از سبد خرید
def cart_remove(request, item_id):
    cart = request.session.get('cart', [])
    if 0 <= item_id < len(cart):
        del cart[item_id]
        request.session['cart'] = cart
        messages.success(request, "آیتم از سبد خرید حذف شد.")
    return redirect('catalog:cart_view')


# افزایش تعداد
def cart_increase(request, item_id):
    cart = request.session.get('cart', [])
    if 0 <= item_id < len(cart):
        cart[item_id]['quantity'] += 1
        request.session['cart'] = cart
    return redirect('catalog:cart_view')


# کاهش تعداد
def cart_decrease(request, item_id):
    cart = request.session.get('cart', [])
    if 0 <= item_id < len(cart) and cart[item_id]['quantity'] > 1:
        cart[item_id]['quantity'] -= 1
        request.session['cart'] = cart
    return redirect('catalog:cart_view')


# جستجو
def search_results(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query, available=True) if query else []
    return render(request, 'catalog/search_results.html', {
        'query': query,
        'products': products
    })


# صفحه تماس و درباره ما
def contact_page(request):
    return render(request, 'catalog/contact.html')

def about_page(request):
    return render(request, 'catalog/about.html')


# پرداخت (نمونه)
def checkout_view(request):
    cart = request.session.get('cart', [])
    return render(request, 'catalog/checkout.html', {'cart': cart})

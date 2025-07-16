from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from catalog.models import Product, PaymentRequest
from users.models import Profile  # در صورت نیاز برای نمایش اطلاعات کاربری
from django.db import transaction

# 🏠 صفحه خانه
def homepage_view(request):
    products = Product.objects.filter(available=True)
    return render(request, 'catalog/homepage.html', {'products': products})

# 📋 ثبت درخواست پرداخت
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

            if amount_val and amount_val >= 1000:
                PaymentRequest.objects.create(
                    user=request.user,
                    amount=amount_val,
                    payment_receipt=receipt,
                    description=description,
                    reference_number=tracking_code,
                    status='pending'
                )
                print("🎉 ثبت انجام شد در مدل PaymentRequest")
                messages.success(request, "پرداخت شما با موفقیت ثبت شد ✅")
            else:
                messages.error(request, "مبلغ نامعتبر یا کمتر از حد مجاز است ❌")
        except Exception as e:
            print("❌ خطا هنگام ذخیره پرداخت:", str(e))
            messages.error(request, "ذخیره پرداخت با مشکل مواجه شد ❌")

        return redirect('catalog:submit_payment')

    return render(request, 'catalog/submit_payment.html')

# ✅ تأیید درخواست پرداخت
@login_required
def approve_payment(request, pk):
    payment = get_object_or_404(PaymentRequest, pk=pk)
    payment.approve()
    messages.success(request, "پرداخت تأیید شد ✅")
    return redirect('catalog:payment_list_admin')

# ❌ رد درخواست پرداخت
@login_required
def reject_payment(request, pk):
    payment = get_object_or_404(PaymentRequest, pk=pk)
    payment.status = 'rejected'
    payment.save()
    messages.error(request, "پرداخت رد شد ❌")
    return redirect('catalog:payment_list_admin')

# 👤 نمای پروفایل
@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})

# 📦 نمای محصول
def product_detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'catalog/product_detail.html', {'product': product})

# 🛍 لیست محصولات
def product_list_view(request):
    products = Product.objects.filter(available=True)
    return render(request, 'catalog/product_list.html', {'products': products})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

from core.utils.sms_service import send_verification_code
from users.forms import TrabiLoginForm, TrabiUserCreationForm, EditProfileForm
from users.models import Address
from catalog.models import CustomerDebt, PaymentRequest
from .models import Order
from catalog.models import Product 
from .forms import (
    PasswordResetForm,
    OTPVerificationForm,
    NewPasswordForm,
    ContactForm,
    PaymentRequestForm
)

import random

User = get_user_model()

# 🔷 صفحه اصلی
def homepage_view(request):
    recent_products = Product.objects.filter(available=True).order_by('-created_at')[:8]
    return render(request, 'catalog/homepage.html', {'recent_products': recent_products})


# 📄 صفحه معرفی
def about_page_view(request):
    return render(request, 'core/about.html')


# 📩 فرم تماس با ما
def contact_page_view(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        messages.success(request, "پیام شما با موفقیت ارسال شد ✅")
        return redirect('core:contact_page')
    return render(request, 'core/contact.html', {'form': form})


# 🔐 ثبت‌نام با OTP
def register_view(request):
    form = TrabiUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        code = str(random.randint(100000, 999999))

        request.session['user_id'] = user.id
        request.session['otp_code'] = code
        request.session['otp_verified'] = False

        send_verification_code(user.phone_number, code)
        messages.success(request, 'ثبت‌نام انجام شد ✅ لطفاً کد تأیید را وارد کنید')

        return redirect('core:verify_otp')
    return render(request, 'core/register.html', {'form': form})


# 🔐 ورود
def login_view(request):
    form = TrabiLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.cleaned_data['user']
        login(request, user)
        return redirect('core:profile')
    return render(request, 'core/login.html', {'form': form})


# 🔓 خروج
@login_required
def logout_view(request):
    logout(request)
    return redirect('core:login')


# 👤 صفحه پروفایل
@login_required
def profile_view(request):
    return render(request, 'core/profile.html')


# 📄 ویرایش اطلاعات پروفایل
@login_required
def edit_profile_view(request):
    form = EditProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'اطلاعات شما به‌روزرسانی شد ✅')
        return redirect('core:profile')
    return render(request, 'core/edit_profile.html', {'form': form})


# 🖼️ ویرایش تصویر پروفایل
@login_required
def edit_profile_image(request):
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            request.user.profile_image = profile_image
            request.user.save()
            messages.success(request, 'تصویر پروفایل آپلود شد ✅')
            return redirect('core:profile')
        messages.error(request, 'هیچ فایلی انتخاب نشده ❌')
    return render(request, 'core/edit_profile_image.html')


# 🔑 تغییر رمز عبور داخل حساب
@login_required
def password_change_view(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'رمز عبور تغییر کرد ✅')
        return redirect('core:profile')
    return render(request, 'core/password_change.html', {'form': form})


# 🔒 بازیابی رمز عبور با OTP
def password_reset_request(request):
    form = PasswordResetForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.cleaned_data['user']
        code = str(random.randint(100000, 999999))

        request.session['user_id'] = user.id
        request.session['otp_code'] = code
        request.session['otp_verified'] = False

        send_verification_code(user.phone_number, f'کد بازیابی شما: {code}')
        messages.success(request, 'کد بازیابی ارسال شد ✅')
        return redirect('core:verify_otp')
    return render(request, 'core/password_reset_form.html', {'form': form})


# 🟩 تأیید OTP
def verify_otp(request):
    form = OTPVerificationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        code = form.cleaned_data['otp_code']
        if code == request.session.get('otp_code'):
            request.session['otp_verified'] = True
            messages.success(request, 'کد تأیید شد ✅')
            return redirect('core:set_new_password')
        messages.error(request, 'کد اشتباه است ❌')
    return render(request, 'core/verify_otp.html', {'form': form})


# 🔐 تنظیم رمز جدید بعد از OTP
def set_new_password(request):
    if not request.session.get('otp_verified'):
        messages.error(request, 'ابتدا باید کد تأیید را وارد کنید')
        return redirect('core:password_reset_request')

    form = NewPasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user_id = request.session.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.set_password(form.cleaned_data['new_password1'])
        user.save()
        messages.success(request, 'رمز جدید ثبت شد ✅')
        return redirect('core:login')
    return render(request, 'core/set_new_password.html', {'form': form})


# 🧾 سفارش‌ها
@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'core/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order})


# 💳 داشبورد مالی
@login_required
def customer_debts_view(request): 
    debt = CustomerDebt.objects.filter(user=request.user).first()
    requests = PaymentRequest.objects.filter(user=request.user).order_by('-created_at')
    approved_requests = PaymentRequest.objects.filter(user=request.user, status='approved')

    total_debt = debt.total_debt if debt else 0
    total_paid = sum([r.amount for r in approved_requests])

    if request.method == 'POST':
        form = PaymentRequestForm(request.POST, request.FILES)
        if form.is_valid():
            pr = form.save(commit=False)
            pr.user = request.user
            pr.status = 'pending'
            pr.save()
            messages.success(request, 'درخواست ثبت شد ✅')
            return redirect('core:customer_debts')
    else:
        form = PaymentRequestForm()

    context = {
        'debt': debt,
        'form': form,
        'requests': requests,
        'total_debt': total_debt,
        'total_paid': total_paid
    }
    return render(request, 'core/financial_dashboard.html', context)


# ✅ تأیید پرداخت توسط مدیر
@login_required
def confirm_payment_view(request, id):
    payment = get_object_or_404(PaymentRequest, id=id)
    payment_was_pending = False

    if payment.status == 'pending':
        payment.status = 'approved'
        payment.save()
        debt = CustomerDebt.objects.filter(user=payment.user).first()
        if debt:
            debt.total_debt = max(debt.total_debt - payment.amount, 0)
            debt.save()
        payment_was_pending = True
        messages.success(request, 'پرداخت تأیید شد و بدهی کاهش یافت ✅')
    else:
        messages.info(request, 'این پرداخت قبلاً بررسی شده است')

    return render(request, 'core/confirm_payment.html', {
        'payment': payment,
        'confirmed': payment_was_pending
    })


# 📍 آدرس‌ها
@login_required
def address_list_view(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'core/address_list.html', {'addresses': addresses})

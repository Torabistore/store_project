# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# فرم‌ها و مدل‌ها
from .forms import CustomUserCreationForm, PasswordResetForm, SetNewPasswordForm, LoginForm
from .models import User

import kavenegar
import random
from django.conf import settings

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'با موفقیت وارد شدید.')
            return redirect('catalog:homepage')  # ارجاع به catalog:homepage
        else:
            messages.error(request, 'شماره موبایل یا رمز عبور اشتباه است.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد.')
            return redirect('catalog:homepage')  # ارجاع به catalog:homepage
        else:
            messages.error(request, 'لطفاً اطلاعات را به درستی وارد کنید.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('catalog:homepage')  # ارجاع به catalog:homepage

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            try:
                user = User.objects.get(mobile_number=mobile_number)
                otp = str(random.randint(100000, 999999))

                try:
                    api = kavenegar.KavenegarAPI(settings.KAVENEGAR_API_KEY)
                    params = {
                        'receptor': mobile_number,
                        'message': f'کد تأیید شما: {otp}',
                    }
                    api.sms_send(params)
                    print(f"DEBUG: OTP for {mobile_number}: {otp}")

                except kavenegar.ApiException as e:
                    messages.error(request, f'خطا در ارسال OTP (Kavenegar): {e}. لطفاً دوباره تلاش کنید.')
                    return render(request, 'accounts/password_reset_form.html', {'form': form})
                except Exception as e:
                    messages.error(request, f'خطا در ارسال OTP: {e}. لطفاً دوباره تلاش کنید.')
                    return render(request, 'accounts/password_reset_form.html', {'form': form})

                request.session['otp'] = otp
                request.session['user_id'] = user.id
                return redirect('accounts:verify_otp')

            except User.DoesNotExist:
                messages.error(request, 'کاربری با این شماره موبایل وجود ندارد.')
        else:
            messages.error(request, 'لطفاً شماره موبایل را به درستی وارد کنید.')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset_form.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        user_id = request.session.get('user_id')
        if otp == session_otp and user_id:
            return redirect('accounts:set_new_password', uidb64=urlsafe_base64_encode(force_bytes(user_id)), token=default_token_generator.make_token(User.objects.get(id=user_id)))
        else:
            messages.error(request, 'کد OTP اشتباه است.')
    return render(request, 'accounts/verify_otp.html')

def set_new_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetNewPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'رمز عبور با موفقیت تغییر کرد.')
                return redirect('accounts:login')
            else:
                messages.error(request, 'لطفاً اطلاعات را به درستی وارد کنید.')
        else:
            form = SetNewPasswordForm(user)
        return render(request, 'accounts/set_new_password.html', {'form': form})
    else:
        messages.error(request, 'لینک نامعتبر است.')
        return redirect('accounts:password_reset')

def homepage_view(request):
    return render(request, 'catalog/homepage.html')  # اصلاح ارجاع به قالب catalog/homepage.html

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def order_list_view(request):
    return render(request, 'accounts/order_list.html')
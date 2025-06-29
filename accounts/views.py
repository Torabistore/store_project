# accounts/views.py

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import login
from django.contrib import messages
from kavenegar import KavenegarAPI, APIException, HTTPException
from django.contrib.auth import logout as auth_logout # <--- این خط اضافه شد

# تمام فرم‌های مورد نیاز را یکجا وارد می‌کنیم
from .forms import PasswordResetRequestForm, VerifyOTPForm, CustomUserCreationForm
from .models import User
import random

# =========== ویوهای مربوط به بازیابی رمز عبور ===========

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            try:
                user = User.objects.get(mobile_number=mobile_number)
                otp_code = random.randint(100000, 999999)
                request.session['otp_code'] = otp_code
                request.session['otp_mobile'] = mobile_number
                
                # ارسال پیامک واقعی با کاوه‌نگار
                try:
                    api = KavenegarAPI(settings.SMS_API_KEY)
                    params = {
                        'sender': settings.SMS_SENDER_NUMBER,
                        'receptor': mobile_number,
                        'message': f'کد بازیابی رمز شما: {otp_code}'
                    }
                    response = api.sms_send(params)
                except Exception as e: 
                    print(f"Kavenegar Error: {e}")
                    messages.error(request, 'خطا در ارسال پیامک. لطفاً با پشتیبانی تماس بگیرید.')
                    return render(request, 'accounts/password_reset_form.html', {'form': form})

                return redirect('accounts:verify_otp')

            except User.DoesNotExist:
                form.add_error('mobile_number', 'کاربری با این شماره همراه یافت نشد.')
        
        return render(request, 'accounts/password_reset_form.html', {'form': form})
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounts/password_reset_form.html', {'form': form})


def verify_otp(request):
    otp_code_session = request.session.get('otp_code')
    mobile_number = request.session.get('otp_mobile')
    if not otp_code_session or not mobile_number:
        return redirect('accounts:password_reset_request')

    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['otp_code']
            if int(entered_code) == otp_code_session:
                request.session['otp_verified'] = True
                return redirect('accounts:set_new_password')
            else:
                form.add_error('otp_code', 'کد وارد شده صحیح نمی‌باشد.')
    else:
        form = VerifyOTPForm()
    return render(request, 'accounts/verify_otp.html', {'form': form})


def set_new_password(request):
    mobile_number = request.session.get('otp_mobile')
    is_verified = request.session.get('otp_verified')
    if not mobile_number or not is_verified:
        return redirect('accounts:password_reset_request')

    user = User.objects.get(mobile_number=mobile_number)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            # پاک کردن اطلاعات یکبار مصرف از حافظه
            if 'otp_code' in request.session: del request.session['otp_code']
            if 'otp_mobile' in request.session: del request.session['otp_mobile']
            if 'otp_verified' in request.session: del request.session['otp_verified']
            
            login(request, user)
            messages.success(request, 'رمز عبور شما با موفقیت تغییر یافت و وارد شدید.')
            return redirect('/')
    else:
        form = SetPasswordForm(user)
    return render(request, 'accounts/set_new_password.html', {'form': form})


# =========== ویو مربوط به ثبت نام ===========

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'ثبت نام شما با موفقیت انجام شد! حالا می‌توانید وارد شوید.')
            login(request, user) # ورود خودکار کاربر بعد از ثبت نام
            return redirect('/') # هدایت به صفحه اصلی
        # اگر فرم نامعتبر بود، فرم با خطاها دوباره رندر می شود
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# =========== ویو جدید مربوط به خروج ===========

def logout_view(request): # <--- این تابع اضافه شد
    auth_logout(request) 
    messages.info(request, "با موفقیت از حساب کاربری خود خارج شدید.") 
    return redirect('accounts:login') # هدایت به صفحه ورود
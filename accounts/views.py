# accounts/views.py
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm # فرم ثبت‌نام سفارشی ما
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login # این خط اضافه شده
from .models import Order

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # کاربر را بلافاصله پس از ثبت‌نام وارد می‌کند
            return redirect('profile') # به صفحه پروفایل هدایت می‌کند
        else:
            # اگر فرم نامعتبر بود، فرم را با خطاها دوباره نمایش بده
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def order_list(request):
    orders = request.user.orders.all()
    context = {
        'orders': orders
    }
    return render(request, 'accounts/order_list.html', context)
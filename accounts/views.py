# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # فرم پیش‌فرض ثبت‌نام جنگو
from django.contrib.auth.decorators import login_required # دکوراتور برای محافظت از صفحات
from .models import Order # وارد کردن مدل Order

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # بعد از ثبت‌نام موفق به صفحه ورود هدایت می‌کند
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required # این دکوراتور اطمینان می‌دهد که فقط کاربران لاگین کرده بتوانند این صفحه را ببینند
def profile(request):
    # در آینده می‌توانید اطلاعات بیشتری از پروفایل کاربر را اینجا نمایش دهید
    return render(request, 'accounts/profile.html')

@login_required
def order_list(request):
    orders = request.user.orders.all() # تمام سفارشات مربوط به کاربر لاگین کرده را دریافت می‌کند
    context = {
        'orders': orders
    }
    return render(request, 'accounts/order_list.html', context)